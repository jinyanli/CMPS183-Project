# -*- coding: utf-8 -*-
db = DAL("sqlite://storage.sqlite")

db.define_table('department',
    Field('name', 'string', unique=True),
    Field('short_name','string', unique=True)
)

db.define_table('course',
    Field('department_id', 'reference department'),
    Field('course_num', 'string'),
    Field('name', 'string', unique=True),
    Field('description', 'text')
)

db.define_table('professor',
    Field('name','string', unique=True, default=None),
    Field('image', 'upload', update=True, authorize=True),
    Field('saltiness', 'double')
)

db.define_table('ucscClass', # 'class' is a python reserved word
    Field('course_id', 'reference course'),
    Field('description', 'text'),
    Field('term'),
    Field('difficulty', 'double'),
    Field('textbook_ids', 'list:reference textbook'),
    Field('professor_id', 'reference professor')
)

db.define_table('classReview',
    Field('user_id', 'reference user'),
    Field('content', 'text', update=True),
    Field('term'),
    Field('rating', 'double')
)

db.define_table('post',
    Field('ucscClass_id', 'reference ucscClass'),
    Field('user_id', 'reference user'),
    Field('title', 'string'),
    Field('body', 'text'),
    Field('price', 'integer') # price is in cents (eg 4000 -> $40)
    Field('image', 'upload')
    Field('datetime', 'datetime')
)

db.define_table('comment',
    Field('user_id', 'reference user'),
    Field('post_id', 'reference post'),
    Field('body', 'text'),
    Field('datetime', 'datetime')
)

db.define_table('user',
    Field('user_id', 'reference user'),
    Field('username', 'string', unique=True),
    Field('image', 'upload', update=True),
    Field('email'),
    Field('password', 'string', length=10),
    Field('year'),
    Field('is_admin','boolean', default=False)
)
db.user.email.requires = IS_EMAIL()

db.define_table('studentGrade',
    Field('user_id', 'reference user'),
    Field('grade', 'integer'),
    Field('ucscClass_id', 'reference ucscClass')
)

db.define_table('professorReview',
    Field('professor_id', 'reference professor'),
    Field('user_id', 'reference user'),
    Field('course_id', 'reference course'),
    Field('term'),
    Field('review','text',update=True),
    Field('rating', 'double'),
    Field('datetime','datetime')
)

db.define_table('note',
    Field('title', 'string'),
    Field('file', 'upload'),
    Field('user_id', 'reference user'),
    Field('course_id','reference course'),
    Field('professor_id', 'reference professor'),
    Field('notetype', 'string'),
    Field('datetime', 'datetime')
)

db.define_table('textbook',
    Field('title', 'string', ondelete='CASCADE'),
    Field('author', 'list:string'),
    Field('publication_year', 'integer'),
    Field('isbn', 'integer', unique=True)
)
