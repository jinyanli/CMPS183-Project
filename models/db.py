db = DAL("sqlite://storage.sqlite")

db.define_table('department',
    Field('name', unique=True),
    Field('short_name'))

db.define_table('course',
    Field('dept_id', 'reference department'),
    Field('course_num', unique=True),
    Field('name'))

db.define_table('class',
    Field('course_id', 'reference course'),
    Field('description'),
    Field('term'),
    Field('difficulty', 'double'),
    Field('textbook_ids', 'reference textbook'),
    Field('professor_id', 'reference professor'))

db.define_table('professor',
    Field('name'),
    Field('image', 'upload'),
    Field('saltiness', 'double'))

db.define_table('student',
    Field('first_name'),
    Field('last_name'))

db.define_table('class_review',
    Field('student_id', 'reference student'),
    Field('text', 'text'),
    Field('term'),
    Field('rating', 'double'))

db.define_table('post',
    Field('class_id', 'reference class'),
    Field('student_id', 'reference student'),
    Field('title'),
    Field('body', 'text'),
    Field('datetime', 'datetime'))

db.define_table('sale_post',
    Field('student_id', 'reference student'),
    Field('title'),
    Field('body', 'text'),
    Field('price', 'integer'),
    Field('image', 'upload'),
    Field('datetime', 'datetime'))

db.define_table('comment',
    Field('student_id', 'reference student'),
    Field('post_id', 'reference post'),
    Field('body', 'text'),
    Field('datetime', 'datetime'))

db.define_table('user',
    Field('student_id', 'reference student'),
    Field('image', 'upload'),
    Field('email'),
    Field('password'),
    Field('year'),
    Field('is_admin', 'boolean'))
db.user.email.requires = IS_EMAIL()

db.define_table('student_grade',
    Field('grade', 'intger'),
    Field('student_id', 'reference student'),
    Field('class_id', 'reference class'))

db.define_table('professor_review',
    Field('professor_id', 'reference professor'),
    Field('user_id', 'reference user'),
    Field('course_id', 'reference course'),
    Field('term'),
    Field('review', 'text'),
    Field('rating', 'double'),
    Field('datetime', 'datetime'))

db.define_table('note',
    Field('title'),
    Field('file', 'upload'),
    Field('user_id', 'reference user'),
    Field('course_id', 'reference course'),
    Field('professor_id', 'reference professor'),
    Field('note_type'),
    Field('datetime', 'datetime'))

db.define_table('textbook',
    Field('title'),
    Field('author'),
    Field('publication_year', 'integer'),
    Field('isbn'))
