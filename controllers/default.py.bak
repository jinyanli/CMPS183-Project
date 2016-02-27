# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import string
import math
from gluon.tools import Crud
crud = Crud(db)

def index():
    response.flash = T("Slug Hero")
    return dict(message=T('Welcome to Slug Hero'))

def showClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.ucscClass.course_id==ucscClass.id).select(orderby=db.ucscClass.year | db.ucscClass.quarter)
    return locals()

def classPage():
    thisClass = db.ucscClass(request.args(0, cast=int)) or redirect(URL('showCourse'))
    courseInfo = db.course(thisClass.course_id)
    thisClassProfessor=db.professor(thisClass.professor_id)
    professors = db(db.professor.department_id==courseInfo.department_id).select(db.professor.ALL, orderby=db.professor.id)
    if thisClassProfessor != None:
        classReviews = db(db.classReview.professor==thisClassProfessor.id).select(db.classReview.ALL, orderby=~db.classReview.yr|~db.classReview.quarter)
        db.classReview.professor.default = thisClassProfessor
    gradeA = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="A-")|(db.classReview.grade=="A")|(db.classReview.grade=="A+")).count()
    gradeB = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="B-")|(db.classReview.grade=="B")|(db.classReview.grade=="B+")).count()
    gradeC = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="C-")|(db.classReview.grade=="C")|(db.classReview.grade=="C+")).count()
    gradeD = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="D-")|(db.classReview.grade=="D")|(db.classReview.grade=="D+")).count()
    gradeF = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="F")).count()
    gradeP = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="P")).count()
    gradeNP = db((db.classReview.ucscClass_id==thisClass.id) & (db.classReview.grade=="NP")).count()
    fall = "Fall"
    winter = "Winter"
    spring = "Spring"
    summer = "Summer"
    user = auth.user
    syllabus = thisClass.syllabus
    if user != None:
        db.classReview.user_id.default = auth.user.id
    db.classReview.ucscClass_id.default = thisClass.id
    form = SQLFORM(db.classReview)
    if form.process(session=None, formname='postReview').accepted:
        response.flash = 'review accepted'
        redirect(URL('classPage', args=request.args(0,cast=int)))
    elif form.errors:
        response.flash = 'Error: your submission is incomplete'
    else:
        if user != None:
            response.flash = 'You may fill in the form to post a review'
    return locals()

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
    uClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.ucscClass.course_id==uClass.id).select(orderby=db.ucscClass.yr | db.ucscClass.quarter)
    fall = "Fall"
    winter = "Winter"
    spring = "Spring"
    summer = "Summer"
    return locals()

def check_term(form):
    q = form.vars.quarter
    y = form.vars.year
    query = db((db.ucscClass.quarter == q) & (db.ucscClass.yr == y)).select()
    if query:
        form.errors.query = 'Term already exists'
        response.flash = 'Term already exists'

def createClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    db.ucscClass.course_id.default = ucscClass.id
    fields = ['syllabus', 'quarter', 'yr', 'difficulty']
    #labels = {'name':'Professor Name'}
    form = SQLFORM(db.ucscClass, fields=fields)
    form.add_button('Back', URL('showClass', args=ucscClass.id))
    if form.process(onvalidation=check_term).accepted:
        response.flash = 'Class added'
        redirect(URL('showClass', args=ucscClass.id))
    info = db(db.ucscClass.course_id==ucscClass.id).select()
    return dict(form=form)

def editClass():
    aClass = db.ucscClass(request.args(0,cast=int)) or redirect(URL('showClass',args=request.args(0,cast=int)))
    form = crud.update(db.ucscClass,aClass,next=URL('showClass',args=aClass.course_id))
    return dict(form=form)

#this function is for adding professor for showProfessor page
def addProfessor():
    crud.messages.submit_button = 'Submit'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.professor, next='showProfessor')
    return locals()

def classPageAddProfessor():
    thisClass = db.ucscClass(request.args(0,cast=int)) or redirect(URL('showClass',args=request.args(0,cast=int)))
    course=db.course(thisClass.course_id)
    db.ucscClass.professor_id.requires = IS_IN_DB(db((db.course.department_id==db.professor.department_id) & (db.course.id==thisClass.course_id)), db.professor.id, '%(first_name)s'+' '+'%(last_name)s', zero=T('choose one'))
    form=SQLFORM(db.ucscClass, thisClass, ignore_rw=True,
                 fields=['professor_id'])
    if form.process().accepted:
       redirect(URL('classPage',args=request.args(0,cast=int)))
    #form for creating a new professor
    db.professor.department_id.default=course.department_id
    fields = ['first_name', 'last_name', 'image']
    form2 = SQLFORM(db.professor, fields=fields)
    if form2.process().accepted:
       db(db.ucscClass.id == thisClass.id).update(professor_id=form2.vars.id)
       redirect(URL('classPage',args=request.args(0,cast=int)))
    elif form2.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form,form2=form2)

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

def testpage():
    form=FORM('Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        response.flash = 'form accepted'
        redirect(URL('default','bookExchange', args=request.vars.name))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    A=30
    return locals()
    #return dict(form=form, A=A)

def viewCourseTopic():
    uCourse = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.courseTopic.board_id==uCourse.id).select()
    return locals()
