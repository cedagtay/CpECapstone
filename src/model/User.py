from sqlalchemy import Column, Integer, String

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    course = Column(String)
    term = Column(String)
    form_number = Column(String)
    email_id = Column(String)
    address = Column(String)
