@auth.requires_login()
def createTopic():
    uCourse = db.course(request.args(0, cast=int)) or redirect(URL('default','viewCourseTopic', args=uCourse.id))
    page = request.args(1, cast=int)
    fields = ['yr', 'quarter', 'title', 'body']
    labels = {'yr' : 'What year?', 'quarter' : 'What quarter?', 'body' : 'What would you like to discuss?', 'title' : 'Message title'}
    db.courseTopic.board_id.default = uCourse.id
    db.courseTopic.op.default = auth.user.id
    form = SQLFORM(db.courseTopic, labels=labels, fields=fields)
    form.add_button('Cancel', URL('default','viewCourseTopic', args=[uCourse.id, page]))
    if form.process().accepted:
        response.flash = 'Post added'
        redirect(URL('default','viewCourseTopic', args=[uCourse.id, page]))
    return locals()