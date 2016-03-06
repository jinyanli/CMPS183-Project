@auth.requires_login()
def showTopic():
	topic = db.courseTopic(request.args(0, cast=int)) or redirect(URL('default','viewCourseTopic', args=uCourse.id))
	page = request.args(1, cast=int)
	db.courseReply.topic_id.default = topic.id
	db.courseReply.op.default = topic.op
	db.courseReply.replyOp.default = auth.user.id
	form = SQLFORM(db.courseReply)
	if form.process().accepted:
	    response.flash = "Post added"
	    db(db.courseTopic.id == topic.id).update(replies=topic.replies+1)
	    redirect(URL('show', 'showTopic', args=[topic.id, page]))

	db.courseTopicReply.replyOp.default = auth.user.id
	replyForm = SQLFORM(db.courseTopicReply)

	if request.env.request_method == 'POST':
		if "x" in request.post_vars.keys():
			session.CourseReplyId = int(request.post_vars["x"])

	if replyForm.process().accepted:
		response.flash = "Post added"
		CourseIdReply = db(db.courseTopicReply.id == replyForm.vars.id).select().first()
		CourseIdReply.update_record(topic_id = session.CourseReplyId)

	return locals()