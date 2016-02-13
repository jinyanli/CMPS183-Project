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
    professors = db().select(db.professor.ALL, orderby=db.professor.id)
    profPic = ""
    prof_id = None
    for item in info:
        for prof in professors:
            if item.professor_id == prof.id:
                profPic = prof.image
                prof_id = prof.id
    classReviews = db(db.profReview.course_id==uClass.id).select()
    if prof_id == None:
        prof_id=1
    profReviews = db(db.profReview.professor_id==prof_id).select()
    reviews = []
    for cRev in classReviews:
        for pRev in profReviews:
            if cRev.id == pRev.id:
                reviews.append(pRev)
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

#this function is for adding professor for showProfessor page
def addProfessor():
    crud.messages.submit_button = 'Submit'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.professor, next='showProfessor')
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
    return dict(form=form)

def viewCourseTopic():
    uCourse = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.courseTopic.board_id==uCourse.id).select()
    return locals()