# -*- coding: utf-8 -*-

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
    Field('description', 'text')
    #format = lambda this: deslugify(db.department(this.department_id).name)+ ' '+this.course_num
    )

db.define_table('professor',
    Field('first_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('last_name', 'string', default=None, requires=(IS_SLUG(), IS_NOT_EMPTY())),
    Field('image', 'upload'),
    Field('department_id', 'reference department'),
    Field('saltiness', 'double')
    )

db.professor.department_id.requires = IS_IN_DB(db, db.department.id, '%(name)s')

quarter=['fall', 'winter', 'spring', 'summer']
db.define_table('ucscClass', # 'class' is a python reserved word
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('syllabus', 'text'),
    Field('quarter', 'string', requires=IS_IN_SET(quarter)),
    Field('yr', 'integer', requires=IS_IN_SET(range(2000, 2101))), # year is a keyword in SQL
    Field('term', 'string'),
    Field('difficulty', 'double'),
    Field('textbook_ids', 'list:reference textbook'),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('datetime', 'datetime'))

db.define_table('classRevieww',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('ucscClass_id', 'reference  ucscClass', readable=False, writable=False),
    Field('body', 'text', update=True),
    Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
    Field('yr', requires=IS_INT_IN_RANGE(2000, 2051)),
    Field('rating', 'double'),
    Field('datetime', 'datetime', readable=False,writable=False, default=request.now))

db.define_table('postt',
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False),
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('title', 'string', notnull=True),
    Field('body', 'text', notnull=True),
    Field('price', 'integer'), # price is in cents (eg 4000 -> $40)
    Field('image', 'upload'),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now))

#comment is a resevered key word. Can't be used
db.define_table('commm',
    Field('user_id', 'reference  auth_user', readable=False, writable=False),
    Field('post_id', 'reference postt', readable=False , writable=False),
    Field('body', 'text'),
    Field('datetime', 'datetime', readable=False,writable=False,default=request.now))


db.define_table('studentGradee',
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('grade', 'list:string'),
    Field('ucscClass_id', 'reference ucscClass', readable=False, writable=False))

gradeRange=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', 'P', 'NP']
db.studentGradee.grade.requires = IS_IN_SET(gradeRange)

#new table for pro
db.define_table('profRevieww',
     Field('professor_id', 'reference professor', readable=False, writable=False),
     Field('user_id', 'reference auth_user', readable=False, writable=False),
     Field('course_id', 'reference course'),
     Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
     Field('yr', requires=IS_INT_IN_RANGE(2000, 2051)),#year
     Field('review', 'text', update=True),
     Field('rating', 'double'),
     Field('datetime', 'datetime', readable=False,writable=False,default=request.now))

#below table doesn't work. don't know why
"""
db.define_table('profReview',
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('course_id', 'reference course'),
    Field('quarter', requires=IS_IN_SET(['Fall', 'Winter', 'Spring', 'Summer'])),
    Field('yr', requires=IS_INT_IN_RANGE(2000, 2051)),#year
    Field('review', 'text', update=True),
    Field('rating', 'double'),
    Field('posted_on', 'datetime', readable=False,writable=False))
db.professorRevieww.rating.requires = IS_FLOAT_IN_RANGE(0, 5)
"""

db.define_table('notee',
    Field('title', 'string'),
    Field('notefile', 'upload'),
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('course_id', 'reference course', readable=False, writable=False),
    Field('professor_id', 'reference professor', readable=False, writable=False),
    Field('notetype', 'string'),
    Field('datetime', 'datetime'))

noteType = ['exam', 'homework', 'class note', 'course material', 'solution', 'other']
db.notee.notetype.requires = IS_IN_SET(noteType)

db.define_table('textbookk',
    Field('title', 'string', ondelete='CASCADE'),
    Field('author', 'list:string'),
    Field('publication_year', 'integer'),
    Field('isbn', 'integer', unique=True))
