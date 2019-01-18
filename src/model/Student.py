from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from Semester import Semester

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))
    semester = Column(Enum(Semester))
    form_number = Column(String)
    email_id = Column(String)
    address = Column(String)
