# -*- coding: utf-8 -*-
# try something like
import string
import math
from gluon.tools import Crud
crud = Crud(db)
POSTS_PER_PAGE = 10

@auth.requires_login()
def showProfile():
    page = request.args(1,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    user = db.auth_user(request.args(0,cast=int)) or redirect(URL(request.vars['controller'], request.vars['function'], args=request.vars['args']))
    if request.vars['fromMenu']=='True':
       fromMenu=True
    else:
       fromMenu=False
    if request.vars['edit']!='True':
        session.controller=request.vars['controller']
        session.function=request.vars['function']
        session.args=request.vars['args']
    numOfPage=int(math.ceil(db(db.profReview.user_id==user.id).count()/10.0))
    reviews =db(db.profReview.user_id==user.id).select(db.profReview.ALL, orderby=~db.profReview.datetime, limitby=(start, stop))
    return locals()

def editProfile():
    user = db.auth_user(request.args(0,cast=int))
    form=SQLFORM(db.auth_user, user, ignore_rw=True,
                 fields=['first_name', 'last_name', 'email', 'term', 'image', 'show_email', 'major', 'second_major', 'minor'])
    if form.process().accepted:
       redirect(URL('showProfile', args=request.args(0,cast=int), vars=dict(edit=True)))
    return dict(form=form)
