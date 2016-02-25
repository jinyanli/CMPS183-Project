from gluon.tools import Crud
import math
crud = Crud(db)

POSTS_PER_PAGE = 50
POSTS_PER_PAGE_COMM = 10
#add a new comment!


def generalForum():
    page = request.args(0,cast=int,default=0)
    count = 0
    swithColor = 1
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE    
    number = int(math.ceil(db(db.post.forumSection=='forum')(db.post.id > 0).count() /50.0))
    if number - page <= 5:
        count = 5-(number - page)

    db.post.status.writable = db.post.status.readable = False
    db.post.price.writable = db.post.price.readable = False
    db.post.image.writable = db.post.image.readable = False
    #forumData = db.post(request.args(0,cast=int)) or redirect(URL('bookExchange'))
    forums = db( db.post.price == None , db.post.status == False).select(orderby =~ db.post.update_time, limitby=(start,stop))
    return locals()

def addForum():
    db.post.user_id.default = auth.user.id
    db.post.forumSection.default="forum"
    db.post.price.writable = db.post.price.readable = False
    db.post.status.writable = db.post.status.readable = False
    db.post.image.writable = db.post.image.readable = False
    form = crud.create(db.post)
    return locals()

def editForum():

    forum = db.post(request.args(0,cast=int))
    #db.post.post_id.default = forum.id
    db.post.price.writable = db.post.price.readable = False
    db.post.status.writable = db.post.status.readable = False
    db.post.image.writable = db.post.image.readable = False
    form = crud.update(db.post, forum, next=URL('showEachForum', args=request.args(0,cast=int)))
    return locals()

@auth.requires_login()
def showEachForum():
     #control the pages
    page = request.args(1,cast=int,default=0)
    start = page*POSTS_PER_PAGE_COMM
    stop = start+POSTS_PER_PAGE_COMM
    count = 0
    forum = db.post(request.args(0,cast=int)) or redirect(URL('generalForum')) 
    number = int(math.ceil(db(db.comm.post_id == forum.id)(db.comm.id > 0).count() /10.0))
    if number - page <= 5:
        count = 5-(number - page)
       
    #comms
    db.comm.user_id.default = auth.user.id
    db.comm.post_id.default = forum.id
    form=SQLFORM(db.comm, record=None,
        deletable=False, linkto=None,
        upload=None, fields=None, labels=None,
        col3={}, submit_button='Post comment',
        delete_label='Check to delete:',
        showid=True, readonly=False,
        comments=True, keepopts=[],
        ignore_rw=False, record_id=None,
        formstyle='bootstrap3_stacked',
        buttons=['submit'], separator=': ')
    if form.process().accepted:
        response.flash = 'your comment is posted'
        updateTimer=db(db.comm.post_id==forum.id).select(db.comm.ALL, orderby=~db.comm.datetime, limitby=(0,1)).first()
        oldTimer = db(db.post.id == forum.id).select().first()
        oldTimer.update_record(update_time = updateTimer.datetime)
        redirect(URL('showEachForum', args=forum.id))
    lenComms  = db(db.comm.post_id==forum.id).select(db.comm.ALL)
    comms  = db(db.comm.post_id==forum.id).select(db.comm.ALL, orderby=db.comm.datetime, limitby=(start,stop))
    forumimages= db(db.forumImage.post_id==forum.id).select(db.forumImage.ALL, orderby=db.forumImage.title)
    #replyComments =  db.forumCommReply(request.args(0,cast=int)) or redirect(URL('generalForum'))

    #commTableInf = db.comm(request.args(0,cast=int)) or redirect(URL('generalForum'))
    #db.forumCommReply.comm_id.default = commTableInf.id
    db.forumCommReply.user_id.default = auth.user.id
    replyForm = SQLFORM(db.forumCommReply, record=None,
        deletable=False, linkto=None,
        upload=None, fields=None, labels=None,
        col3={}, submit_button='Reply',
        delete_label='Check to delete:',
        showid=True, readonly=False,
        comments=True, keepopts=[],
        ignore_rw=False, record_id=None,
        formstyle='bootstrap3_stacked',
        buttons=['submit'], separator=': ')
    if replyForm.process().accepted:
        redirect(URL('showEachForum', args=request.args(0,cast=int)))

    return locals()

@auth.requires_login()
def replyComment():
    commTableInf = db.comm(request.args(0,cast=int)) or redirect(URL('generalForum'))
    db.forumCommReply.comm_id.default = commTableInf.id
    db.forumCommReply.user_id.default = auth.user.id
    form = SQLFORM(db.forumCommReply, record=None,
        deletable=False, linkto=None,
        upload=None, fields=None, labels=None,
        col3={}, submit_button='Reply',
        delete_label='Check to delete:',
        showid=True, readonly=False,
        comments=True, keepopts=[],
        ignore_rw=False, record_id=None,
        formstyle='bootstrap3_stacked',
        buttons=['submit'], separator=': ')
    if form.process().accepted:
        redirect(URL('showEachForum', args=request.args(1,cast=int)))
    return locals()

@auth.requires_login()
def editForumComment():
    editComm=db.comm(request.args(0,cast=int)) or redirect(URL('showEachForum'))
    if auth.user_id == editComm.user_id:
       form = crud.update(db.comm, editComm, next=URL('showEachForum', args=request.args(1,cast=int)))
    return dict(form=form)

@auth.requires_login()
def bookExchange():
    page = request.args(0,cast=int,default=0)
    count = 0
    start = page*POSTS_PER_PAGE_COMM
    stop = start+POSTS_PER_PAGE_COMM
    #show_all = request.args(0) == 'all'
    q = db.post
    listings = db(db.post.forumSection=='bookExchange').select(orderby =~ db.post.datetime, limitby=(start,stop))
    number = int(math.ceil(db(db.post.forumSection=='bookExchange')(db.post.id > 0).count() /10.0))
    if number - page <= 5:
        count = 5-(number - page)
    #a = FORM(INPUT(_name='a', requires=IS_INT_IN_RANGE(0, 10)),
    #   INPUT(_type='submit'), value _action=URL('page_two'))

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
    enterNumber= FORM('Go to page:', INPUT(_name='num', requires= IS_INT_IN_RANGE(1,number+1),_size ='1'),
                               INPUT(_type='submit', _value= "Go"))
    if enterNumber.process().accepted:
        redirect(URL(args=(int(request.vars.num) -1)))
    elif enterNumber.errors:
        response.flash = 'enter a number'
    return locals()


@auth.requires_login()
def showBook():
    #control the pages
    page = request.args(1,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    count = 0
    book = db.post(request.args(0,cast=int)) or redirect(URL('bookExchange'))
    number = int(math.ceil(db(db.comm.post_id == book.id)(db.comm.id > 0).count() /10.0))
    if number - page <= 5:
        count = 5-(number - page)
    #comms
    db.comm.user_id.default = auth.user.id
    db.comm.post_id.default = book.id
    form=SQLFORM(db.comm, record=None,
        deletable=False, linkto=None,
        upload=None, fields=None, labels=None,
        col3={}, submit_button='Post',
        delete_label='Check to delete:',
        showid=True, readonly=False,
        comments=True, keepopts=[],
        ignore_rw=False, record_id=None,
        formstyle='bootstrap3_stacked',
        buttons=['submit'], separator=': ')
    #crud.settings.captcha = None
    #crud.settings.showid = False
    #crud.settings.label_separator = ':'
    #crud.messages.submit_button = 'Post'
    #crud.settings.formstyle = 'divs'
    #form = crud.create(db.comm)
    if form.process().accepted:
        response.flash = 'your comment is posted'
        redirect(URL('showBook', args=book.id))
    comments = db(db.comm.post_id == book.id).select(db.comm.ALL, orderby=~db.comm.datetime, limitby=(start,stop))
    return locals()

@auth.requires_login()
def addBookItem():
    db.post.user_id.default = auth.user.id
    db.post.forumSection.default = 'bookExchange'
    crud.messages.submit_button = 'Place on market'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.post).process(next='bookExchange')
    return locals()

def manageBookItems():
    grid = SQLFORM.grid(db.post)
    return locals()

@auth.requires_login()
def editBookItem():
    bookItem=db.post(request.args(0,cast=int)) or redirect(URL('showBook'))
    if auth.user_id == bookItem.user_id:
       form = crud.update(db.post, bookItem, next=URL('showBook', args=request.args(0,cast=int)))
    return dict(form=form)

@auth.requires_login()
def editComment():
    editComm=db.comm(request.args(0,cast=int)) or redirect(URL('showBook'))
    if auth.user_id == editComm.user_id:
       form = crud.update(db.comm, editComm, next=URL('showBook', args=request.args(1,cast=int)))
    return dict(form=form)

@auth.requires_login()
def manageItems():
    grid = SQLFORM.grid(db.post)
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
