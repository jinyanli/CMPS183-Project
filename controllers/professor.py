# -*- coding: utf-8 -*-
# try something like
import string
import math
from gluon.contrib.populate import populate
from gluon.tools import Crud
crud = Crud(db)

POSTS_PER_PAGE = 10
def deslugify(_slug):
    """
    Convert a SLUG back into standard format.
    e.g. "electrical-engineering" => "Electrical Engineering"
    """
    return string.capwords(_slug.replace('-', ' '))

def showProfessor():
    depts = db().select(db.department.ALL, orderby=db.department.name)
    for dept in depts:
        dept.name=deslugify(dept.name)
    profs = db().select(db.professor.ALL, orderby=db.professor.first_name)
    return locals()

@auth.requires_login()
def addProfessor():
    crud.messages.submit_button = 'Submit'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.professor, next='showProfessor')
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
    avgHelpfulness=db.profReview.helpfulness.avg()
    helpfulness=db(db.profReview.professor_id==prof.id).select(avgHelpfulness).first()[avgHelpfulness]
    avgClarity=db.profReview.clarity.avg()
    clarity=db(db.profReview.professor_id==prof.id).select(avgClarity).first()[avgClarity]
    avgEasiness=db.profReview.easiness.avg()
    easiness=db(db.profReview.professor_id==prof.id).select(avgEasiness).first()[avgEasiness]
    return locals()

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
       redirect(URL('professorReview', args=request.args(0,cast=int)))
    return locals()

@auth.requires_login()
def professorEdit():
    prof = db.professor(request.args(0,cast=int)) or redirect(URL(request.vars['currentPage'], args=request.args(0,cast=int)))
    form = crud.update(db.professor,prof,next=URL(request.vars['currentPage'], args=request.args(0,cast=int)))
    return locals()

@auth.requires_login()
def editProfessorReview():
    profreview=db.profReview(request.args(0,cast=int)) or redirect(URL('professorReview', args=request.args(1,cast=int)))
    if auth.user_id == profreview.user_id:
       crud.settings.formstyle='bootstrap3_stacked'
       form = crud.update(db.profReview, profreview, next=URL('professorReview', args=request.args(1,cast=int)))
    return dict(form=form)
