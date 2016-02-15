from gluon.tools import Crud
import math
crud = Crud(db)

POSTS_PER_PAGE = 10
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

@auth.requires_login()
def bookExchange():
    page = request.args(0,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    #show_all = request.args(0) == 'all'
    q = db.post
    listings = db(db.post.forumSection=='bookExchange').select(orderby =~ db.post.datetime, limitby=(start,stop))
    number = int(math.ceil(db(db.post.forumSection=='bookExchange')(db.post.id > 0).count() /10.0))
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
        response.flash = 'form has errors'
    return locals()


@auth.requires_login()
def showBook():
    book = db.post(request.args(0,cast=int)) or redirect(URL('bookExchange'))
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
        formstyle='table3cols',
        buttons=['submit'], separator=': ')
    #crud.settings.captcha = None
    #crud.settings.showid = False
    #crud.settings.label_separator = ':'
    #crud.messages.submit_button = 'Post'
    #crud.settings.formstyle = 'divs'
    #form = crud.create(db.comm)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.comm.post_id == book.id).select(db.comm.ALL, orderby=~db.comm.datetime)
    return locals()

@auth.requires_login()
def addBookItem():
    db.post.user_id.default = auth.user.id
    db.post.forumSection.default = 'bookExchange'
    crud.messages.submit_button = 'Place on market'
    crud.settings.keepvalues = True
    crud.settings.label_separator = ' :'
    crud.settings.formstyle = 'ul'
    form = crud.create(db.post)
    return locals()

def manageBookItems():
    grid = SQLFORM.grid(db.post)
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)