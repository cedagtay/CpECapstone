from tkinter import *
from sqlalchemy import *

class App():
    def __init__(self, database, facerecog, executor):
        names = database.retrieve_names()
        user_id = facerecog.recognize(names)
        
