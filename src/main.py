from tkinter import *
from App import App
from WBDatabase import Database
from FaceRecog import FaceRecog
def main():
    tk = Tk()
    database = Database()
    facerecog = FaceRecog("./opencv_data/haarcascade/haarcascade_frontalface_alt.xml", "./user_image")
    app = App(tk, database, facerecog)
    

if __name__ == '__main__':
    main()
