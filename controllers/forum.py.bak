from gluon.tools import Crud
crud = Crud(db)
def generalForum():
    forums = db( db.post.price == None , db.post.status == False).select(orderby = ~db.post.datetime)
    db.post.status.writable = db.post.status.readable = False
    db.post.price.writable = db.post.price.readable = False
    db.post.image.writable = db.post.image.readable = False
    form = crud.create(db.post).process()
    return locals()
