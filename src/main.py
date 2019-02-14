from tkinter import Tk
from App import App
from Database import Database
from FaceRecog import FaceRecog
from concurrent.futures import ThreadPoolExecutor
def main():
    database = Database("mysql://cpedev@localhost/cpedb")
    facerecog = FaceRecog("./opencv_data/haarcascade/haarcascade_frontalface_default.xml", "./opencv_data/haarcascade/haarcascade_frontalface_alt.xml", "./opencv_data/trainer/trainer.yml", "./user_image", database)
    executor = ThreadPoolExecutor(max_workers=1)
    app = App(database, facerecog, executor)
    

if __name__ == '__main__':
    main()
