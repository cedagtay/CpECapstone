from sqlalchemy import Column, String, Integer

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    
