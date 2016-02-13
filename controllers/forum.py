from gluon.tools import Crud
crud = Crud(db)

#add a new comment!


def generalForum():
    forums = db( db.post.price == None , db.post.status == False).select(orderby = db.post.datetime)
    db.post.status.writable = db.post.status.readable = False
    db.post.price.writable = db.post.price.readable = False
    db.post.image.writable = db.post.image.readable = False
    return locals()

def addForum():
    db.post.forumSection.default="forum"
    db.post.price.writable = db.post.price.readable = False
    db.post.status.writable = db.post.status.readable = False
    db.post.image.writable = db.post.image.readable = False
    form = crud.create(db.post).process(next='generalForum')
    return locals()

def editForum():

    forum = db.post(request.args(0,cast=int))
    #db.post.post_id.default = forum.id
    db.post.price.writable = db.post.price.readable = False
    db.post.status.writable = db.post.status.readable = False
    db.post.image.writable = db.post.image.readable = False
    form = crud.update(db.post, forum, next=URL('showEachForum', args=request.args(0,cast=int)))
    return locals()

def showEachForum():
    forum = db.post(request.args(0,cast=int)) or redirect(URL('generalForum'))
    comms  = db(db.comm.post_id==forum.id).select(db.comm.ALL, orderby=db.comm.datetime)
    return locals()

def addComment():
    forum = db.post(request.args(0,cast=int)) or redirect(URL('generalForum'))
    db.comm.post_id.default = forum.id
    form = crud.create(db.comm)
    if form.process().accepted:
        redirect(URL('showEachForum', args=request.args(0,cast=int)))
    return locals()

#still a issue here
def editComment():
    forum = db.comm(request.args(0,cast=int)).post_id #or redirect(URL('showEachForm', args=request.args(0,cast=int)))
    comm = db.comm(request.args(0,cast=int))
    form = SQLFORM(db.comm, comm)
    form.add_button('back', URL('showEachForum', args = forum))
    db.comm.id.writable=db.comm.id.readable=False
    if form.process().accepted:
        redirect(URL('showEachForum', args=forum))
    return locals()
