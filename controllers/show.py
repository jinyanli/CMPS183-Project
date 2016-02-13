def showTopic():
	topic = db.courseTopic(request.args(0, cast=int)) or redirect(URL('default','viewCourseTopic', args=uCourse.id))
	return locals()