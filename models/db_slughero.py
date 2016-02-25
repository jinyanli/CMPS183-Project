# -*- coding: utf-8 -*-
from gluon.contrib.populate import populate
import string
import math

def deslugify(_slug):
    """
    Convert a SLUG back into standard format.
    e.g. "electrical-engineering" => "Electrical Engineering"
    """
    return string.capwords(_slug.replace('-', ' '))

db.define_table('department',
    Field('name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('short_name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    format = '%(name)s')

db.define_table('course',
    Field('department_id', 'reference department', readable=False, writable=False),
    Field('course_num', 'string', requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('name', 'string', unique=True, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('description', 'text'),
    format = lambda this: deslugify(db.department(this.department_id).name)+ ' '+this.course_num
    )

db.define_table('professor',
    Field('first_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('last_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('image', 'upload'),
    Field('department_id', 'reference department'),
    Field('saltiness', 'double', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),#keep track of who created the professor
    Field('datetime', 'datetime', readable=False,writable=False, default=request.now),
    format = '%(first_name)s'+' '+'%(last_name)s'
    )

db.professor.department_id.requires = IS_IN_DB(db, db.department.id, '%(name)s')

quarter=['fall', 'winter', 'spring', 'summer']
db.define_table('ucscClass', # 'class' is a python reserved word
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('syllabus', 'text'),
    Field('quarter', 'string', requires=IS_IN_SET(quarter)),
    Field('yr', 'integer', requires=IS_IN_SET(range(2000, 2101))), # year is a keyword in SQL
    Field('term', 'string'),
    Field('difficulty', 'double', readable=False, writable=False),
    Field('enjoyment', 'double', readable=False, writable=False),
    Field('textbook_ids', 'list:reference textbook'),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('datetime', 'datetime', readable=False,writable=False, default=request.now))

db.define_table('classReview',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('ucscClass_id', 'reference  ucscClass', readable=False, writable=False),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('body', 'text', update=True),
    Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
    Field('yr', requires=IS_INT_IN_RANGE(2000, 2051)),
    Field('difficulty', 'double'),
    Field('enjoyment', 'double'),
    Field('datetime', 'datetime', readable=False,writable=False, default=request.now))

db.define_table('post',
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False),
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('title', 'string', notnull=True),
    Field('forumSection', 'string', readable=False, writable=False),#to tell whether the post belong textbookExchange or generalDiscussion
    Field('body', 'text', notnull=True),
    Field('price', 'integer'), # price is in cents (eg 4000 -> $40)
    Field('status','boolean', default=False),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now),
    Field('update_time', 'datetime', readable=False,writable=False,default=request.now),
    Field('image', 'upload'),
    format = '%(title)s')

#UPDATE db['post'] SET update_time = datetime

#db['comm'].drop()
#db.commit()
#comment is a resevered key word. Can't be used
db.define_table('comm',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('post_id', 'reference post', readable=False , writable=False),
    Field('body', 'text', requires= IS_NOT_EMPTY()),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now))

db.define_table('forumCommReply',
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('comm_id', 'reference comm', readable=False, writable=False),
    Field('datetime', 'datetime', readable=False, writable=False, default=request.now),
    Field('body', 'text',requires= IS_NOT_EMPTY()))

db.define_table('studentGrade',
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('grade', 'list:string'),
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now)
    )

gradeRange=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', 'P', 'NP']
db.studentGrade.grade.requires = IS_IN_SET(gradeRange)


db.define_table('profReview',
     Field('professor_id', 'reference professor', readable=False, writable=False),
     Field('user_id', 'reference auth_user', readable=False, writable=False),
     Field('course_id', 'reference course'),
     Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
     Field('yr', requires=IS_IN_SET(range(2000, 2101))),#year
     Field('review', 'text', update=True),
     Field('helpfulness', requires=IS_IN_SET([1,2,3,4,5])),
     Field('clarity', requires=IS_IN_SET([1,2,3,4,5])),
     Field('easiness', requires=IS_IN_SET([1,2,3,4,5])),
     Field('rating', 'double', readable=False,writable=False,
            compute=lambda r: (float(r['helpfulness'])+float(r['clarity'])+float(r['easiness']))/3.0),
     Field('datetime', 'datetime', readable=False,writable=False,default=request.now))

db.define_table('note',
    Field('title', 'string'),
    Field('notefile', 'upload'),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now))

db.define_table('noteFolder',
     Field('title', 'string'),
     Field('body', 'text'),
     Field('note_id', 'reference note'),
     Field('user_id', 'reference auth_user', readable=False, writable=False),
     Field('course_id', 'reference course', readable=False, writable=False),
     Field('professor_id', 'reference professor', readable=False, writable=False),
     Field('notetype', 'string'),
     Field('datetime', 'datetime', readable=False,writable=False,compute=request.now))
noteType = ['exam', 'homework', 'class note', 'course material', 'solution', 'other']
db.noteFolder.notetype.requires = IS_IN_SET(noteType)

db.define_table('textbook',
    Field('title', 'string', ondelete='CASCADE'),
    Field('author', 'list:string'),
    Field('publication_year', 'integer'),
    Field('isbn', 'integer', unique=True))

db.define_table('courseTopic',
    Field('board_id', 'reference course', readable=False, writable=False),
    Field('title', 'string'),
    Field('quarter', 'string', requires=IS_IN_SET(quarter)),
    Field('yr', 'integer', requires=IS_IN_SET(range(2000, 2101))),
    Field('op', 'reference auth_user', readable=False, writable=False),
    Field('datePosted', 'datetime', readable=False, writable=False, default=request.now),
    Field('body', 'text'),
    Field('replies', 'integer', default=0, readable=True, writable=False))

db.define_table('courseReply',
    Field('topic_id', 'reference courseTopic', readable=False, writable=False),
    Field('op', 'reference auth_user', readable=False, writable=False),
    Field('replyOp', 'reference auth_user', readable=False, writable=False),
    Field('datePosted', 'datetime', readable=False, writable=False, default=request.now),
    Field('body', 'text'))

db.define_table('courseTopicReply',
    Field('topic_id', 'reference courseReply', readable=False, writable=False),
    Field('replyOp', 'reference auth_user', readable=False, writable=False),
    Field('datePosted', 'datetime', readable=False, writable=False, default=request.now),
    Field('body', 'text'))

db.define_table('conversation',
    Field('user1', 'reference auth_user', readable=False, writable=False),
    Field('user2', 'reference auth_user', readable=False, writable=False))

db.define_table('privateMessage',
    Field('conversation_id', 'reference conversation', readable=False, writable=False),
    Field('sender_id', 'reference auth_user', readable=False, writable=False),
    Field('recipient_id', 'reference auth_user', readable=False, writable=False),
    Field('posted_on', 'datetime', readable=False, writable=False, default=request.now),
    Field('body', 'text',requires=IS_NOT_EMPTY()))

db.define_table('forumImage',
    Field('post_id', 'reference post', readable=False , writable=False),
    Field('title', 'string', requires= IS_NOT_EMPTY()),
    Field('image', 'upload')
    )

#populate(db.post,100)
#db(db.profReview.rating>5).delete()
