from sqlalchemy import *
from datetime import datetime
class Database():
    metadata = MetaData()
    courses = Table('courses', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('name', String(255), nullable = False)
    )
    students = Table('students', metadata,
                     Column('id', Integer, primary_key = True),
                     Column('name', String(255)),
                     Column('course', Integer, ForeignKey('courses.id'), nullable = False),
                     Column('semester', Integer),
                     Column('form_no', Integer),
                     Column('contact_no', String(12)),
                     Column('email_address', String(255)),
                     Column('address', String(255))
    )
    
    logs = Table('logs', metadata,
                 Column('id', Integer, primary_key = True),
                 Column('student_id', Integer, ForeignKey('students.id'), nullable = False),
                 Column('datetime', DateTime, nullable = False, index = True)
    )
    
    subjects = Table('subjects', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('name', String(255), nullable = False)
    )
    
    rooms = Table('rooms', metadata,
                  Column('id', Integer, primary_key = True),
                  Column('number', String(3), nullable = False)
    )
    
    room_subject = Table('room_subject', metadata,
                         Column('id', Integer, primary_key = True),
                         Column('room_id', Integer, ForeignKey('rooms.id'), nullable = False),
                         Column('subject_id'), Integer, ForeignKey('subjects.id'),
                         Column('start_time', Time, nullable = False),
                         Column('end_time', Time, nullable = False)
    )
    
    def __init__(self, constr):
        self.engine = create_engine(constr)
        self.metadata.create_all(self.engine)

    def insert_data(self, name, course, sem, form_no, contact_no, email_id, address):
        new_user = self.students.insert().values(
            name = name, course = course, semester = sem,
            form_no = form_no, contact_no = contact_no,
            email_address = email_id, address = address)
        conn = self.engine.connect()
        result = conn.execute(new_user)
        return result.inserted_primary_key[0]

    def retrieve_names(self):
        student_names = select([self.students.c.id, self.students.c.name])
        conn = self.engine.connect()
        result = conn.execute(student_names)
        for row in result:
            print(str(row))
        return result

    def retrieve_name(self, student_id):
        student_name = select([self.students.c.name]).where(self.students.c.id == student_id)
        conn = self.engine.connect()
        result = conn.execute(student_name).fetchone()
        return result[0]

    def insert_log(self, student_id):
        new_log = self.logs.insert().values(student_id = student_id, datetime = datetime.now())
        conn = self.engine.connect()
        result = conn.execute(new_log)
