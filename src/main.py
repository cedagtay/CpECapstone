from tkinter import Tk
from sqlalchemy import *
from App import App
from Database import Database
from FaceRecog import FaceRecog
from reportlab import *
from concurrent.futures import ThreadPoolExecutor
def main():
    tk = Tk()
    database = Database("mysql://cpedev@localhost/cpedb")
    facerecog = FaceRecog("./opencv_data/haarcascade/haarcascade_frontalface_default.xml", "./opencv_data/haarcascade/haarcascade_frontalface_alt.xml", "./opencv_data/trainer/trainer.yml", "./user_image", database)
    executor = ThreadPoolExecutor(max_workers=1)
    app = App(tk, database, facerecog, executor)
    

if __name__ == '__main__':
    main()
