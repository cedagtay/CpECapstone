from tkinter import *
from tkinter.messagebox import showinfo
from sqlalchemy import *
from itertools import groupby
import datetime as DT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table 

class App():  
    # Function for clearing the 
    # contents of text entry boxes 
    def clear(): 
        # clear the content of text entry box 
        name_field.delete(0, END) 
        course_field.delete(0, END) 
        sem_field.delete(0, END) 
        form_no_field.delete(0, END) 
        contact_no_field.delete(0, END) 
        email_id_field.delete(0, END) 
        address_field.delete(0, END) 

    def __init__(self, root, database, facerecog, executor):
        
        root.title("Registration Form")
        root.geometry("500x300") 
        
        # create a Form label 
        #heading = Label(root, text="Form", bg="white") 
        
        # create a Name label 
        name_label = Label(root, text="Name", bg="white") 
        
        # create a Course label 
        course_label = Label(root, text="Course", bg="white") 
        
        # create a Semester label 
        sem_label = Label(root, text="Semester", bg="white") 
        
        # create a Form No. lable 
        form_no_label = Label(root, text="Form No.", bg="white") 
        
        # create a Contact No. label 
        contact_no_label = Label(root, text="Contact No.", bg="white") 
        
        # create a Email id label 
        email_id_label = Label(root, text="Email id", bg="white") 
        
        # create a address label 
        address_label = Label(root, text="Address", bg="white") 
        
        # grid method is used for placing 
        # the widgets at respective positions 
        # in table like structure . 
        name_label.grid(row=1, column=0) 
        course_label.grid(row=2, column=0) 
        sem_label.grid(row=3, column=0) 
        form_no_label.grid(row=4, column=0) 
        contact_no_label.grid(row=5, column=0) 
        email_id_label.grid(row=6, column=0) 
        address_label.grid(row=7, column=0) 
        
        # create a text entry box 
        # for typing the information 
        name_field = Entry(root) 
        course_field = Entry(root) 
        sem_field = Entry(root) 
        form_no_field = Entry(root) 
        contact_no_field = Entry(root) 
        email_id_field = Entry(root) 
        address_field = Entry(root) 

        # grid method is used for placing 
        # the widgets at respective positions 
        # in table like structure . 
        name_field.grid(row=1, column=1, ipadx="100") 
        course_field.grid(row=2, column=1, ipadx="100") 
        sem_field.grid(row=3, column=1, ipadx="100") 
        form_no_field.grid(row=4, column=1, ipadx="100") 
        contact_no_field.grid(row=5, column=1, ipadx="100") 
        email_id_field.grid(row=6, column=1, ipadx="100") 
        address_field.grid(row=7, column=1, ipadx="100")

        def submit():
            name = name_field.get()
            course = course_field.get()
            sem = sem_field.get()
            form_no = form_no_field.get()
            contact_no = contact_no_field.get()
            email_id = email_id_field.get()
            address = address_field.get()
            if(name == "" and course == "" and sem == "" and
               form_no == "" and contact == "" and email_id == "" and
               address == ""): 
                print("empty input")
            else:
                id = database.insert_data(name, course, sem, form_no,
                                     contact_no, email_id, address)
                name_field.delete(0, END) 
                course_field.delete(0, END) 
                sem_field.delete(0, END) 
                form_no_field.delete(0, END) 
                contact_no_field.delete(0, END) 
                email_id_field.delete(0, END) 
                address_field.delete(0, END)
                database.retrieve_names()
                facerecog.capture(name, id)
                facerecog.train()
                
        def recognize():
            names = database.retrieve_names()
            user_id = facerecog.recognize(names)
            name = database.retrieve_name(user_id)
            showinfo("Window", "Welcome " + name)
            
            
        def report():
            doc = SimpleDocTemplate("report.pdf", pagesize=letter)
            today = DT.date.today()
            ago = today - DT.timedelta(days=7)
            daterange = [str((today - DT.timedelta(days=day))) for day in range(0,7)]
            daterange.reverse()
            rows = database.generate_report(today, ago)
            datas = [
                ['Students Attendance Sheet','','','','','','','Weekly Report'],
                [],[],
                [' ']+daterange]
            elements = []
            for user, dates in groupby(rows, lambda l: l[0]):
                data = [user]
                date_list = list(dates)
                date_list_length = len(date_list)
                for day in daterange:
                    counter = 0
                    for date in date_list:
                        counter+=1
                        if day == str(date[1]):
                            data.append('Present')
                            counter = 0
                            break
                        elif counter == date_list_length:
                            print(date[1])
                            data.append('Absent')
                            counter = 0
                datas.append(data)
            print(datas)
            tab = Table(datas)
            elements.append(tab)
            doc.build(elements)
                
                
        # create a Submit Button and place into the root window 
        submit = Button(root, text="Register", fg="Black", 
                        bg="White", command=submit) 
        submit.grid(row=8, column=1)

        login = Button(root, text="Login", fg="Black",
                       bg="White", command=recognize)
        login.grid(row=9, column=1)

        report = Button(root, text="Generate Report", fg="Black",
                        bg="White", command=report)
                
        report.grid(row=10, column=1)
        
        # start the GUI 
        root.mainloop() 
        
