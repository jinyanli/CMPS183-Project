@auth.requires_login()
def createTopic():
    uCourse = db.course(request.args(0, cast=int)) or redirect(URL('default','viewCourseTopic', args=uCourse.id))
    fields = ['yr', 'quarter', 'title', 'body']
    labels = {'yr' : 'What year?', 'quarter' : 'What quarter?', 'body' : 'What would you like to discuss?', 'title' : 'Message title'}
    db.courseTopic.board_id.default = uCourse.id
    db.courseTopic.op.default = auth.user.id
    form = SQLFORM(db.courseTopic, labels=labels, fields=fields)
    form.add_button('Back', URL('default','viewCourseTopic', args=uCourse.id))
    if form.process().accepted:
        response.flash = 'Post added'
        redirect(URL('default','viewCourseTopic', args=uCourse.id))
    return locals()

@auth.requires_login()
def createReply():
    topic = db.courseTopic(request.args(0, cast=int)) or redirect(URL('show', 'showTopic', args=topic.id))
    db.courseReply.topic_id.default = topic.id
    db.courseReply.op.default = topic.op
    db.courseReply.replyOp.default = auth.user.id
    form = SQLFORM(db.courseReply)
    form.add_button('back', URL('show', 'showTopic', args=topic.id))
    if form.process().accepted:
        response.flash = "Post added"
        db(db.courseTopic.id == topic.id).update(replies=topic.replies+1)
        redirect(URL('show', 'showTopic', args=topic.id))
    return locals()

@auth.requires_login()
def createReplyReply():
    topic = db.courseReply(request.args(0, cast=int)) or redirect(URL('show', 'showTopic', args=topic.topic_id))
    db.courseTopicReply.topic_id.default = topic.id
    db.courseTopicReply.replyOp.default = auth.user.id
    form = SQLFORM(db.courseTopicReply)
    form.add_button('back', URL('show', 'showTopic', args=topic.topic_id))
    if form.process().accepted:
        response.flash = "Post added"
        redirect(URL('show', 'showTopic', args=topic.topic_id))
    return locals()
