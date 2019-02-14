import os
from sqlalchemy import *
from datetime import datetime

engine = create_engine(os.environ['SQLALCHEMY_URL'])
metadata = MetaData()
metadata.create_all(engine)

courses = Table('courses', metadata,
                Column('id', Integer, primary_key = True),
                Column('name', String(255), nullable = False)
)
students = Table('students', metadata,
                 Column('id', Integer, primary_key = True),
                 Column('name', String(255)),
                 Column('course', Integer, ForeignKey('courses.id'), nullable = False),
                 Column('year', Integer, nullable = False),
                 Column('sem', Integer, nullable = False),
                 Column('semester', Integer),
                 Column('form_no', Integer),
                 Column('contact_no', String(12)),
                 Column('email_address', String(255)),
                 Column('address', String(255))
)

logs = Table('logs', metadata,
             Column('id', Integer, primary_key = True),
             Column('student_id', Integer, ForeignKey('students.id'), nullable = False),
             Column('time', Time, nullable = False, index = True),
             Column('date', Date, nullable = False, index = True)
)


subjects = Table('subjects', metadata,
                 Column('id', Integer, primary_key = True),
                 Column('name', String(255), nullable = False, unique = True)
)

subject_year_sem = Table('subject_year_sem', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('subject_id', Integer, ForeignKey('subjects.id'), nullable = False),
                         Column('course_id', Integer, ForeignKey('courses.id'), nullable = False),
                         Column('year', Integer, nullable = False),
                         Column('sem', Integer, nullable = False)
)

rooms = Table('rooms', metadata,
              Column('id', Integer, primary_key = True),
              Column('number', String(3), nullable = False)
)

room_subject = Table('room_subject', metadata,
                     Column('id', Integer, primary_key = True),
                     Column('room_id', Integer, ForeignKey('rooms.id'), nullable = False),
                     Column('subject_id', Integer, ForeignKey('subjects.id'), nullable = False),
                     Column('start_time', Time, nullable = False),
                     Column('end_time', Time, nullable = False)
)

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(255), nullable = False, unique = True),
              Column('password', String(255), nullable = False)
)

professors = Table('professors', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('first_name', String(255), nullable=False),
                   Column('last_name', String(255), nullable=False)
)

professor_room_subject = Table('professor_room_subject', metadata,
                               Column('id', Integer, primary_key=True)
)

def insert_data(name, course, sem, form_no, contact_no, email_id, address):
    new_user = students.insert().values(
        name = name, course = course, semester = sem,
        form_no = form_no, contact_no = contact_no,
        email_address = email_id, address = address)
    conn = engine.connect()
    result = conn.execute(new_user)
    return result.inserted_primary_key[0]

def retrieve_names():
    student_names = select([students.c.id, students.c.name])
    conn = engine.connect()
    result = conn.execute(student_names)
    for row in result:
        print(str(row))
    return result
    
def retrieve_name(student_id):
    student_name = select([students.c.name]).where(students.c.id == student_id)
    conn = engine.connect()
    result = conn.execute(student_name).fetchone()
    return result[0]

def insert_log(student_id):
    new_log = logs.insert().values(student_id = student_id, datetime = datetime.now())
    conn = engine.connect()
    result = conn.execute(new_log)

def register_user(username, password):
    new_user = users.insert().values(username = username, password = password)
    conn = engine.connect()
    result = conn.execute(new_user)
    return result

def login_user(username, password):
    user_logged = select([users.c.id, users.c.username]).where(users.c.username == username and users.c.password == password)
    conn = engine.connect()
    result = conn.execute(user_logged).fetchone()
    return result[0]

engine = create_engine(os.environ['SQLALCHEMY_URL'])
metadata.create_all(engine)
