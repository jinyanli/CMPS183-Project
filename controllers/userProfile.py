# -*- coding: utf-8 -*-
# try something like
import string
import math
from gluon.tools import Crud
crud = Crud(db)
POSTS_PER_PAGE = 10

"""
def isEmpty(form):
    if form.vars.body is None:
       form.errors.body = 'cannot be empty'
"""
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
    if request.vars['edit']!='True' and request.vars['pageButton']!='True':
        session.controller=request.vars['controller']
        session.function=request.vars['function']
        session.args=request.vars['args']
    numOfPage=int(math.ceil(db(db.profReview.user_id==user.id).count()/10.0))
    reviews =db(db.profReview.user_id==user.id).select(db.profReview.ALL, orderby=~db.profReview.datetime, limitby=(start, stop))
    db.privateMessage.sender_id.default = auth.user.id
    db.privateMessage.recipient_id.default = user.id
    messageForm=SQLFORM(db.privateMessage)
    if messageForm.process().accepted:
       session.flash = 'record inserted'
    elif messageForm.errors:
       session.flash = 'form has errors'
    else:
       session.flash= 'please fill the form'
    return locals()

def editProfile():
    user = db.auth_user(request.args(0,cast=int))
    form=SQLFORM(db.auth_user, user, ignore_rw=True,
                 fields=['first_name', 'last_name', 'email', 'term', 'image', 'show_email', 'major', 'second_major', 'minor'])
    if form.process().accepted:
       redirect(URL('showProfile', args=request.args(0,cast=int), vars=dict(edit=True, fromMenu=request.vars['fromMenu'])))
    return dict(form=form)

def inbox():
    messages = db(db.privateMessage.sender_id==request.args(0,cast=int)).select()
    return dict(messages=messages)
