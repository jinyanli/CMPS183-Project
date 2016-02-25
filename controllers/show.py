@auth.requires_login()
def showTopic():
	topic = db.courseTopic(request.args(0, cast=int)) or redirect(URL('default','viewCourseTopic', args=uCourse.id))
	db.courseReply.topic_id.default = topic.id
	db.courseReply.op.default = topic.op
	db.courseReply.replyOp.default = auth.user.id

	#for replies
	form = SQLFORM(db.courseReply)
	form.add_button('back', URL('show', 'showTopic', args=topic.id))
	if form.process().accepted:
		response.flash = "Post added"
		db(db.courseTopic.id == topic.id).update(replies=topic.replies+1)
		redirect(URL('show', 'showTopic', args=topic.id))

	#for quick replies
	replys = db(db.courseReply.topic_id==topic.id).select()
	form2 = SQLFORM(db.courseTopicReply)
	form2.add_button('back', URL('show', 'showTopic', args=topic.id))
	form2.vars.topic_id = replys[0].id
	form2.vars.replyOp = auth.user.id
	if form2.process().accepted:
		response.flash = "Post added"
		redirect(URL('show', 'showTopic', args=topic.id))
	return locals()