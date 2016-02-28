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
    user = db.auth_user(request.args(0,cast=int)) or redirect(URL(request.vars['controller'],
           request.vars['function'], args=request.vars['args']))
    if request.vars['fromMenu']=='True':
       fromMenu=True
    else:
       fromMenu=False
    if request.vars['edit']!='True' and request.vars['pageButton']!='True':
        session.controller=request.vars['controller']
        session.function=request.vars['function']
        session.args=request.vars['args']
    numOfPage=int(math.ceil(db(db.profReview.user_id==user.id).count()/10.0))
    reviews =db(db.profReview.user_id==user.id).select(db.profReview.ALL,
             orderby=~db.profReview.datetime, limitby=(start, stop))
    db.privateMessage.sender_id.default = auth.user.id
    db.privateMessage.recipient_id.default = user.id
    messageForm=SQLFORM(db.privateMessage)
    if messageForm.process().accepted:
        if auth.user.id != user.id:
            query1 = db((db.conversation.user1 == auth.user.id)
                     & (db.conversation.user2 == user.id)).count()
            query2 = db((db.conversation.user1 == user.id)
                     & (db.conversation.user2 == auth.user.id)).count()
            if query1==0 and query2 == 0:
               db.conversation.insert(user1=auth.user.id, user2=user.id)
               conversation=db.conversation(user1=auth.user.id, user2=user.id)
            else:
               query1=db((db.conversation.user1 == auth.user.id) & (db.conversation.user2 == user.id)).count()
               query2=db((db.conversation.user1 == user.id) & (db.conversation.user2 == auth.user.id)).count()
               if query1==0:
                   conversation=db.conversation(user1 = user.id,user2 = auth.user.id)
               else:
                   conversation=db.conversation(user2 = user.id,user1 = auth.user.id)
            #redirect(URL('default','testpage', args=db.privateMessage(messageForm.vars.id)))
            db(db.privateMessage.id==messageForm.vars.id).update(conversation_id=conversation.id)
        session.flash = 'record inserted'
    elif messageForm.errors:
       session.flash = 'form has errors'
    else:
       session.flash= 'please fill the form'
    return locals()

@auth.requires_login()
def editProfile():
    user = db.auth_user(request.args(0,cast=int))
    form=SQLFORM(db.auth_user, user, ignore_rw=True,
                 fields=['first_name', 'last_name', 'email', 'term',
                      'image', 'show_email', 'major', 'second_major', 'minor'])
    if form.process().accepted:
       redirect(URL('showProfile', args=request.args(0,cast=int),
                     vars=dict(edit=True, fromMenu=request.vars['fromMenu'])))
    return dict(form=form)

@auth.requires_login()
def messageBox():
    count = db.privateMessage.body.count()
    messages = db(((db.privateMessage.sender_id==auth.user_id)
               & (db.privateMessage.recipient_id!=auth.user_id))
               | ((db.privateMessage.recipient_id==auth.user_id)
               & (db.privateMessage.sender_id!=auth.user_id) )).select(db.privateMessage.ALL,
               count,
               groupby=db.privateMessage.conversation_id,
               orderby=~db.privateMessage.posted_on)
    return locals()

@auth.requires_login()
def showMessages():
    recipient=db.auth_user(request.args(0,cast=int))
    messages=db(db.privateMessage.conversation_id==request.args(1,cast=int)).select(orderby=~db.privateMessage.posted_on)
    db.privateMessage.sender_id.default = auth.user.id
    db.privateMessage.recipient_id.default = recipient.id
    db.privateMessage.conversation_id.default = request.args(1,cast=int)
    form=SQLFORM(db.privateMessage)
    if form.process().accepted:
       session.flash = 'Message sent'
       redirect(URL('showMessages', args=[request.args(0,cast=int),request.args(1,cast=int)]))
    return locals()
