# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    dept = db().select(db.department.ALL, orderby=db.department.name)
    form = SQLFORM(db.department)
    if form.process().accepted:
        response.flash = 'Department added'
    return dict(dept=dept, form=form)

def show():
    dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    #db.course.department_id.default = dept.id
    info = db(db.course.department_id==dept.id).select()
    return dict(dept=dept, info=info)

def addCourse():
    dept = db.department(request.args(0,cast=int)) or redirect(URL('index'))
    db.course.department_id.default = dept.id
    form = SQLFORM(db.course)
    if form.process().accepted:
        response.flash = 'Course added'
        redirect(URL('show', args=dept.id))
    info = db(db.course.course_id==dept.id).select()
    return dict(dept=dept, info=info, form=form)

def showClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    info = db(db.UCSCclass.course_id==ucscClass.id).select()
    return dict(ucscClass=ucscClass, info=info)

def addClass():
    ucscClass = db.course(request.args(0, cast=int)) or redirect(URL('index'))
    db.UCSCclass.course_id.default = ucscClass.id
    form = SQLFORM(db.UCSCclass)
    if form.process().accepted:
        response.flash = 'Class added'
        redirect(URL('showClass', args=ucscClass.id))
    info = db(db.UCSCclass.course_id==ucscClass.id).select()
    return dict(ucscClass=ucscClass, info=info, form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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
