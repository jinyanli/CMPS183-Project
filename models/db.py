# -*- coding: utf-8 -*-
db = DAL("sqlite://storage.sqlite")

db.define_table('department',
   Field('department_id'),
   Field('name', 'string', unique=True),
   Field('short_name','string', unique=True)
   )

db.define_table('course',
   Field('course_id'),
   Field('department_id', 'reference department'),
   Field('course_num','integer',unique=True),
   Field('name', 'string', unique=True),
   Field('description', 'text'))

db.define_table('professor',
   Field('professor_id'),
   Field('name','string',unique=True, default=None),
   Field('image', 'upload', update=True, authorize=True),
   Field('saltiness', 'double'))

db.define_table('UCSCclass', # 'class' is a python reserved word
   Field('UCSCclass_id'),
   Field('course_id', 'reference course'),
   Field('description', 'text'),
   Field('term'),
   Field('difficulty','double'),
   Field('textbook_id', 'list:reference textbook', unique=True),
   Field('professor_id', 'reference professor'))

db.define_table('student',
   Field('student_id'),
   Field('first_name', 'string'),
   Field('last_name', 'string'))

db.define_table('classReview',
   Field('classReview_id'),
   Field('student_id', 'reference student'),
   Field('content','text',update=True),
   Field('term'),
   Field('rating', 'double'))

db.define_table('post',
   Field('post_id'),
   Field('UCSCclass_id', 'reference UCSCclass'),
   Field('student_id', 'reference student'),
   Field('title','string'),
   Field('body','text'),
   Field('datetime', 'datetime'))

db.define_table('salePost',
   Field('salePost_id'),
   Field('student_id', 'reference student'),
   Field('title','string'),
   Field('body','text'),
   Field('price', 'double'),
   Field('image', 'upload'),
   Field('datetime', 'datetime'))

db.define_table('comment',
   Field('comment_id'),
   Field('student_id', 'reference student'),
   Field('post_id', 'reference post'),
   Field('body','text'),
   Field('datetime', 'datetime'))


db.define_table('user',
   Field('user_id'),
   Field('student_id', 'reference student'),
   Field('image', 'upload', update=True),
   Field('email'),
   Field('password', 'string', length=10),
   Field('year'),
   Field('is_admin','boolean'))
db.user.email.requires = IS_EMAIL()

db.define_table('studentGrade',
   Field('studentGrade_id'),
   Field('student_id', 'reference student'),
   Field('grade', 'double'),
   Field('UCSCclass_id', 'reference UCSCclass'))

db.define_table('professorReview',
   Field('professorReview_id'),
   Field('professor_id', 'reference professor'),
   Field('user_id', 'reference user'),
   Field('course_id','reference course'),
   Field('term'),
   Field('review','text',update=True),
   Field('rating', 'double'),
   Field('datetime','datetime'))

db.define_table('note',
   Field('note_id'),
   Field('title','string'),
   Field('file','upload'),
   Field('user_id', 'reference user'),
   Field('course_id','reference course'),
   Field('professor_id', 'reference professor'),
   Field('notetype', 'string'),
   Field('datetime','datetime'))

db.define_table('textbook',
   Field('textbook_id'),
   Field('title','string',ondelete='CASCADE'),
   Field('author','list:string'),
   Field('publication_year','integer'),
   Field('isbn', 'integer',unique=True))
