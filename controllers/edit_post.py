def edit_post():
	this_post = db.courseTopic(request.args(0, cast=int)) or redirect(URL('show', 'showTopic', args=this_post.id))
	page = request.args(1, cast=int)
	form = SQLFORM(db.courseTopic, this_post, delete_label='Check to delete', deletable=True)
	form.add_button("Cancel", URL('show', 'showTopic', args=[this_post.id, page]))
	if form.process().accepted:
		redirect(URL('show', 'showTopic', args=[this_post.id, page]))
	return locals()

def edit_reply():
	thread = request.args(1, cast=int)
	this_post = db.courseReply(request.args(0, cast=int)) or redirect(URL('show', 'showTopic', args=thread))
	page = request.args(2, cast=int)
	form = SQLFORM(db.courseReply, this_post, delete_label='Check to delete', deletable=True)
	form.add_button("Cancel", URL('show', 'showTopic', args=[thread, page]))
	if form.process().accepted:
		redirect(URL('show', 'showTopic', args=[thread, page]))
	return locals()

def edit_reply_reply():
	thread = request.args(1, cast=int)
	this_post = db.courseTopicReply(request.args(0, cast=int)) or redirect(URL('show', 'showTopic', args=thread))
	page = request.args(2, cast=int)
	form = SQLFORM(db.courseTopicReply, this_post, delete_label='Check to delete', deletable=True)
	form.add_button("Cancel", URL('show', 'showTopic', args=[thread, page]))
	if form.process().accepted:
		redirect(URL('show', 'showTopic', args=[thread, page]))
	return locals()