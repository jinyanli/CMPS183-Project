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

POSTS_PER_PAGE = 10

def index():
    response.flash = T("Slug Hero")
    return dict(message=T('Welcome to Slug Hero'))

def bookExchange():
    page = request.args(0,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    #show_all = request.args(0) == 'all'
    i = 0
    number = int(math.ceil(db()(db.post.id > 0).count() /10.0))
    q = db.post
    listings = db().select(orderby = db.post.title, limitby=(start,stop))
    #a = FORM(INPUT(_name='a', requires=IS_INT_IN_RANGE(0, 10)),
    #	INPUT(_type='submit'), value _action=URL('page_two'))

    #a.add_button('Back', URL('other_page'))
    #if show_all:
    #button = A('Show available items', _class="btn btn-info", _href=URL('default', 'bookExchange'))
    #else:
    #    button = A('Show all items', _class="btn btn-info", _href=URL('default', 'bookExchange', args=['all']))

    #if show_all:
    #    q = db.post
    #    listings = db().select(orderby = db.post.title, limitby=(start,stop))
    #else:
    #    q=(db.post.status == True)
    #    listings = db(db.post.status == True).select(orderby = db.post.title, limitby=(start,stop))

    form = SQLFORM.grid(q,
        args=request.args[:1],
        fields=[db.post.title,
                    db.post.title,
                    db.post.body,
               ],
        editable=False, deletable=False,
        paginate=10,
        csv=False,
        create=False,
        searchable=False
        )
    return locals()

def showClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.ucscClass.course_id==ucscClass.id).select(orderby=db.ucscClass.year | db.ucscClass.quarter)
    return locals()

def classPage():
    uClass = db.ucscClass(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.ucscClass.course_id==uClass.id).select()
    classReview = db(db.classReview.ucscClass_id==uClass.id).select()
    return locals()

def showBook():
    image = db.post(request.args(0,cast=int)) or redirect(URL('bookExchange'))
    return locals()

def addBookItem():
    crud.messages.submit_button = 'Place on market'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.post)
    return locals()

def manageBookItems():
    grid = SQLFORM.grid(db.post)
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
    course = db.course(request.args(0,cast=int)) or redirect(URL('showClass',args=request.args(0,cast=int)))
    classes = db(db.ucscClass.course_id==course.id).select(orderby=db.ucscClass.yr,limitby=(0,100))
    return locals()

def showProfessor():
    depts = db().select(db.department.ALL, orderby=db.department.name)
    for dept in depts:
        dept.name=deslugify(dept.name)
    profs = db().select(db.professor.ALL, orderby=db.professor.first_name)
    return locals()

@auth.requires_login()
def professorEdit():
    prof = db.professor(request.args(0,cast=int)) or redirect(URL(request.vars['currentPage'], args=request.args(0,cast=int)))
    form = crud.update(db.professor,prof,next=URL(request.vars['currentPage'], args=request.args(0,cast=int)))
    return locals()

#function for professorReview page
def professorReview():
    page = request.args(1,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    prof= db.professor(request.args(0,cast=int)) or redirect(URL('showProfessor'))
    dept=deslugify(db.department(prof.department_id).name)
    deptname=db.department(prof.department_id).short_name
    numOfPage=int(math.ceil(db(db.profReview.professor_id==prof.id).count()/10.0))
    reviews =db(db.profReview.professor_id==prof.id).select(db.profReview.ALL, orderby=~db.profReview.datetime, limitby=(start, stop))
    return locals()

#function for posting a review for a professor for postProfessorReview page
@auth.requires_login()
def postProfessorReview():
    prof= db.professor(request.args(0,cast=int)) or redirect(URL('professorReview', args=request.args(0,cast=int)))
    db.profReview.user_id.default = auth.user.id
    db.profReview.professor_id.default = prof.id
    deptname=db.department(prof.department_id).short_name
    rep=deptname.upper()+' '+'%(course_num)s'
    db.profReview.course_id.requires = IS_IN_DB(db(db.course.department_id==prof.department_id), db.course.id,rep,zero=T('choose one'))
    form = SQLFORM(db.profReview)
    if form.process().accepted:
       avg=db.profReview.rating.avg()
       saltiness=db(db.profReview.professor_id==prof.id).select(avg).first()[avg]
       db(db.professor.id == prof.id).update(saltiness=saltiness)
       session.flash = 'review added'
       redirect(URL('default','professorReview', args=request.args(0,cast=int)))
    return locals()

#function for edit a review in the professor page
@auth.requires_login()
def editProfessorReview():
    profreview=db.profReview(request.args(0,cast=int)) or redirect(URL('professorReview', args=request.args(1,cast=int)))
    if auth.user_id == profreview.user_id:
       form = crud.update(db.profReview, profreview, next=URL('professorReview', args=request.args(1,cast=int)))
    return dict(form=form)

#this function is for adding professor for showProfessor page
def addProfessor():
    crud.messages.submit_button = 'Submit'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.professor, next='showProfessor')
    return locals()

#Jason's function
def professorCreate():
    db.professor.department_id.default = request.args(0,cast=int)
    redirect = "showprofessor/%s" % request.args(0,cast=int)
    crud.messages.submit_button = 'Add Professor'
    crud.settings.label_separator = ' :'
    form = crud.create(db.professor)
    return locals()

#below are helen's functions for creating general discussion forum
#some of them doesn't work
def showPost():
    posts = db().select(db.post.ALL, orderby=db.post.datetime)
    return locals()

@auth.requires_login()
def postCreate():
    db.post.ucscClass_id.default = request.args(0,cast=int)
    form = crud.create(db.post,next=URL('showPost'))
    return locals()

@auth.requires_login()
def postEdit():
    post = db.post(request.args(0,cast=int)) or redirect(URL('showPost'))
    form = crud.update(db.course,course,next='showPost')
    return locals()


def showComm():
    comms = db().select(db.comm.ALL, orderby=db.comm.datetime)
    return locals()

@auth.requires_login()
def commCreate():
    db.comm.post_id_id.default = request.args(0,cast=int)
    form = crud.create(db.comm,next=URL('showComm'))
    return locals()

@auth.requires_login()
def commEdit():
    comm = db.comm(request.args(0,cast=int)) or redirect(URL('showComm'))
    form = crud.update(db.comm,comm,next='showComm')
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

def testpage()

    return locals()
