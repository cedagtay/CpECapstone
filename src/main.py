from tkinter import *
from App import App
from WBDatabase import Database
def main():
    tk = Tk()
    database = Database()
    app = App(tk, database)
    

if __name__ == '__main__':
    main()
