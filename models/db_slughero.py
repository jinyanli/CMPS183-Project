# -*- coding: utf-8 -*-
db.define_table('department',
    Field('name', 'string'),
    Field('short_name','string'))
"""
db.define_table('course',
    Field('department_id', 'reference department',readable=False,writable=False),
    Field('course_num', 'string'),
    Field('name', 'string', unique=True),
    Field('description', 'text'))

db.define_table('professor',
    Field('name','string', unique=True, default=None),
    Field('image', 'upload', update=True, authorize=True),
    Field('saltiness', 'double'),
    #auth.signature?
               )

db.define_table('ucscClass', # 'class' is a python reserved word
    Field('course_id', 'reference course',readable=False,writable=False),
    Field('description', 'text'),
    Field('term'),
    Field('difficulty', 'double'),
    Field('textbook_ids', 'list:reference textbook'),
    Field('professor_id', 'reference professor',readable=False,writable=False),
    Field('user_id', 'reference db.auth_user'),
    Field('datetime', 'datetime'))

db.define_table('classReview',
    Field('user_id', 'reference  db.auth_user'),
    Field('content', 'text', update=True),
    Field('term'),
    Field('rating', 'double'),
    Field('datetime', 'datetime'))

db.define_table('post',
    Field('ucscClass_id', 'reference ucscClass',eadable=False,writable=False),
    Field('user_id', 'reference  db.auth_user',eadable=False,writable=False),
    Field('title', 'string',notnull=True),
    Field('body', 'text',notnull=True),
    Field('price', 'integer'), # price is in cents (eg 4000 -> $40)
    Field('image', 'upload'),
    Field('datetime', 'datetime'))

db.define_table('comment',
    Field('user_id', 'reference  db.auth_user',readable=False,writable=False),
    Field('post_id', 'reference post',readable=False,writable=False),
    Field('body', 'text'),
    Field('datetime', 'datetime'))
gradeRange=['A+','A','A-','B+','B','B-','C+','C','C-','D','F']


db.define_table('studentGrade',
    Field('user_id', 'reference db.auth_user'),
    Field('grade', 'integer'),
    Field('ucscClass_id', 'reference ucscClass'))
db.studentGrade.grade.requires = IS_IN_SET(grade_range)


db.define_table('professorReview',
    Field('professor_id', 'reference professor',readable=False,writable=False),
    Field('user_id', 'reference db.auth_user',readable=False,writable=False),
    Field('course_id', 'reference course',readable=False,writable=False),
    Field('term'),
    Field('review','text',update=True),
    Field('rating', 'double'),
    Field('datetime','datetime'))
db.professorReview.rating.requires = IS_DOUBLE_IN_RANGE(0,5)

noteType = ['exam', 'homework', 'class note', 'course material','solution','other']
db.define_table('note',
    Field('title', 'string'),
    Field('file', 'upload'),
    Field('user_id', 'reference user'),
    Field('course_id','reference course'),
    Field('professor_id', 'reference professor'),
    Field('notetype', 'string'),
    Field('datetime', 'datetime'))
db.note.notetype.requires = IS_IN_SET(noteType)

db.define_table('textbook',
    Field('title', 'string', ondelete='CASCADE'),
    Field('author', 'list:string'),
    Field('publication_year', 'integer'),
    Field('isbn', 'integer', unique=True))
"""
