# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import string
from gluon.tools import Crud
crud = Crud(db)

def index():
    response.flash = T("Slug Hero")
    return dict(message=T('Welcome to Slug Hero'))

def showDepartment():
    depts = db().select(db.department.ALL, orderby=db.department.name)
    for dept in depts:
        dept.name=deslugify(dept.name)

    return locals()

@auth.requires_login()
def departmentCreate():
    form = crud.create(db.department,next='showDepartment')
    return locals()

@auth.requires_login()
#@auth.requires_membership('admin')
def departmentEdit():
    department = db.department(request.args(0,cast=int)) or redirect(URL('showDepartment'))
    form = crud.update(db.department,department,next='showDepartment')
    return locals()

def showCourse():
    dept = db.department(request.args(0,cast=int)) or redirect(URL('showDepartment'))
    courses = db(db.course.department_id==dept.id).select(orderby=db.course.name,limitby=(0,100))
    return locals()

@auth.requires_login()
def courseCreate():
    db.course.department_id.default = request.args(0,cast=int)
    #redirect='showCourse/'+request.args(0,cast=int)
    form = crud.create(db.course,next=URL('showCourse',args=request.args(0,cast=int)))
    return locals()

@auth.requires_login()
def courseEdit():
    course = db.course(request.args(0,cast=int)) or redirect(URL('showCourse',args=request.args(0,cast=int)))
    form = crud.update(db.course,course,next='showCourse')
    return locals()

def showCourse():
    dept = db.department(request.args(0)) or redirect(URL('showDepartment'))
    dept.name = deslugify(dept.name)
    courses = db(db.course.department_id==dept.id).select(orderby=db.course.name,limitby=(0,100))
    return locals()

def showClass():
    course = db.course(request.args(0,cast=int)) or redirect(URL('showCourse',args=request.args(0,cast=int)))
    classes = db(db.ucscClass.course_id==course.id).select(orderby=db.ucscClass.yr,limitby=(0,100))
    return locals()

def createClass():
    db.ucscClass.course_id.default = request.args(0,cast=int)
    dept_id=db(db.course.id==db.ucscClass.course_id).select(db.course.department_id)
    db.professor.department_id.default = dept_id
    form=SQLFORM.factory(db.ucscClass,db.professor)
    if form.process().accepted:
        response.flash = 'class added'
        redirect(URL('showClass', request.args(0,cast=int)))
    return locals()

def editClass():
    course = db.course(request.args(0,cast=int)) or redirect(URL('showClass',args=request.args(0,cast=int)))
    classes = db(db.ucscClass.course_id==course.id).select(orderby=db.ucscClass.year_,limitby=(0,100))
    return locals()

def showProfessor():
    profs = db().select(db.professor.ALL, orderby=db.professor.first_name)
    return locals()

def professorEdit():
    prof = db.professor(request.args(0,cast=int)) or redirect(URL('showProfessor'))
    form = crud.update(db.professor,prof,next='showProfessor')
    return locals()

def professorReview():

    prof= db.professor(request.args(0,cast=int)) or redirect(URL('showProfessor'))
    dept=deslugify(db.department(prof.department_id).name)

    if auth.user:
       db.profReview.user_id.default = auth.user.id
       db.profReview.professor_id.default = prof.id
       #fields = ['description', 'quarter', 'year', 'difficulty']

       deptname=db.department(prof.department_id).short_name
       rep=deptname.upper()+' '+'%(course_num)s'
       db.profReview.course_id.requires = IS_IN_DB(db(db.course.department_id==prof.department_id), db.course.id,rep,zero=T('choose one'))
       message=TAG("<b>Log In To Post A Review</b>")
       form = SQLFORM(db.profReview).process() if auth.user else message
       if form.process().accepted:
           response.flash = 'review added'
           redirect(URL('professorReview', request.args(0,cast=int)))

    reviews = db().select(db.profReview.ALL, orderby=db.profReview.datetime)

    return locals()

@auth.requires_login()
#def professorCreate():
    #dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    #db.course.department_id.default = dept.id
#    form = SQLFORM(db.professor)
#    if form.process().accepted:
#        response.flash = 'Professor added'
#        redirect(URL('showProfessor'))
    #info = db(db.course.course_id==dept.id).select()
#    return locals()

def addProfessor():
    crud.messages.submit_button = 'Submit'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.professor, next='showProfessor')
    return locals()

def professorCreate():
    db.professor.department_id.default = request.args(0,cast=int)
    redirect = "showprofessor/%s" % request.args(0,cast=int)
    crud.messages.submit_button = 'Add Professor'
    crud.settings.label_separator = ' :'
    form = crud.create(db.professor)
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def user():
    return dict(form=auth())


def deslugify(_slug):
    """
    Convert a SLUG back into standard format.
    e.g. "electrical-engineering" => "Electrical Engineering"
    """
    return string.capwords(_slug.replace('-', ' '))
