import locale
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from klases import MyLabel, MyLabelIvesti, MyEntry, MyCombobox, MyRButton, DivisionValues, StudyValues

from sqlalchemy.orm import sessionmaker
from tkcalendar import DateEntry
from database import DuomenuBaze, engine
Session = sessionmaker(bind=engine)
session = Session()

class Ivesti:
    def __init__(self, master):
        self.master = master
        self.canvas = master.canvas

    def add_canvas_elements_ivesti(self):
        locale.setlocale(locale.LC_TIME, 'eu')
        student_label = MyLabel(self.canvas, text="NAUJAS STUDENTAS")
        line = tk.Canvas(self.canvas, width=300, height=1, bg="white", highlightthickness=0)
        name_label = MyLabelIvesti(self.canvas, text="VARDAS")
        last_name_label = MyLabelIvesti(self.canvas, text="PAVARDĖ")
        birth_label = MyLabelIvesti(self.canvas, text="GIMIMO DATA")
        student_since_label = MyLabelIvesti(self.canvas, text="STUDENTAS NUO")
        division_label = MyLabelIvesti(self.canvas, text="PADALINYS")
        study_label = MyLabelIvesti(self.canvas, text="STUDIJOS")
        member_label = MyLabelIvesti(self.canvas, text="TARYBOS NARYS")
        password_label = MyLabelIvesti(self.canvas, text="SLAPTAŽODIS")

        self.name_entry = MyEntry(self.canvas, width=20)
        self.last_name_entry = MyEntry(self.canvas, width=20)
        self.birth_entry = DateEntry(self.canvas, selectmode='day', width=18, background='#3f4f4f',
                                     selectforeground='white',
                                     selectbackground='#3f4f4f', foreground='white', date_pattern='yyyy-mm-dd',
                                     borderwidth=2, cursor='top_left_arrow')
        self.birth_entry.bind("<Key>", self.disable_keyboard_input)
        selected_date = self.birth_entry.get_date()
        self.formatted_date = selected_date.strftime("%Y-%m-%d")
        print(f"Selected Date: {self.formatted_date}")
        self.student_since_entry = DateEntry(self.canvas, selectmode='day', width=18, background='#3f4f4f',
                                             selectforeground='white',
                                             selectbackground='#3f4f4f', foreground='white', date_pattern='yyyy-mm-dd',
                                             borderwidth=2, cursor='top_left_arrow')
        self.student_since_entry.bind("<Key>", self.disable_keyboard_input)
        selected_date_student_since = self.student_since_entry.get_date()
        self.formatted_date_student_since = selected_date_student_since.strftime("%Y-%m-%d")
        print(f"studentas nuo {self.formatted_date_student_since}")
        self.division_entry = MyCombobox(self.canvas, values=DivisionValues.division_choices, width=18)
        self.study_entry = MyCombobox(self.canvas, values=StudyValues.study_choices, width=18)
        self.member_entry = MyCombobox(self.canvas, values=['Taip', 'Ne'], width=18)
        self.password_entry = MyEntry(self.canvas, width=20)
        patvirtinti_button = MyRButton(self.canvas, text="Patvirtinti", command=self.patvirtinti_click)

        student_label.place(x=85, y=10)
        line.place(x=25, y=35)
        name_label.place(x=50, y=100)
        last_name_label.place(x=50, y=125)
        birth_label.place(x=50, y=150)
        student_since_label.place(x=50, y=175)
        division_label.place(x=50, y=200)
        study_label.place(x=50, y=225)
        member_label.place(x=50, y=250)
        password_label.place(x=50, y=275)
        self.name_entry.place(x=160, y=100)
        self.last_name_entry.place(x=160, y=125)
        self.birth_entry.place(x=160, y=150)
        self.student_since_entry.place(x=160, y=175)
        self.division_entry.place(x=160, y=200)
        self.study_entry.place(x=160, y=225)
        self.member_entry.place(x=160, y=250)
        self.password_entry.place(x=160, y=275)
        patvirtinti_button.place(x=160, y=300)


    def patvirtinti_click(self):


        # gauti ivestas reiksmes
        name = self.name_entry.get().title()
        last_name = self.last_name_entry.get().title()
        birth_date_str = self.birth_entry.get()
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        student_since_str = self.student_since_entry.get()
        student_since = datetime.strptime(student_since_str, "%Y-%m-%d").date()
        division = self.division_entry.get()
        study = self.study_entry.get()
        member = self.member_entry.get()
        password = self.password_entry.get()

        # aspsaugos
        if not name or not last_name or not division or not study or not member or not password or not birth_date or not student_since:
            messagebox.showerror("Klaida", "Visi laukai turi būti užpildyti.")
            return

        # apsauga tikrina ar vardas / pavarde tik raides
        if not name.isalpha() or not last_name.isalpha():
            messagebox.showerror("Klaida", "Vardas ir pavardė gali turėti tik raides.")
            return

        messagebox.showinfo("Patvirtinta", "Naujas studentas pridėtas sėkmingai.")

        new_student = DuomenuBaze(
            name=name,
            last_name=last_name,
            birth_date=birth_date,
            student_since=student_since,
            division=division,
            study=study,
            member=member,
            password=password
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_student)
        session.commit()
        session.close()


    def disable_keyboard_input(self, event):
        return "break"
