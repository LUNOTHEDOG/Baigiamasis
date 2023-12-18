from tkinter import messagebox
import tkinter as tk
from klases import MyLabel, MyCombobox, MyRButton
from sqlalchemy.orm import session, sessionmaker
from database import DuomenuBaze, engine

Session = sessionmaker(bind=engine)
session = Session()


class Pasalinti:
    def __init__(self, master):
        self.master = master
        self.canvas = master.canvas

    def add_canvas_elements_pasalinti(self):
        student_label = MyLabel(self.canvas, text="PAŠALINTI STUDENTĄ")
        line = tk.Canvas(self.canvas, width=300, height=1, bg="white", highlightthickness=0)
        self.label_info_text = "Pasirinkite studentą iš sąrašo, kurį norite pašalinti"
        self.label_info = tk.Label(self.canvas, text=self.label_info_text, wraplength=300, justify="left",
                                   bg="#00272B", fg="white", font=("Helvetica", 10))

        students = session.query(DuomenuBaze).all()
        student_names = [f"{student.name} {student.last_name}" for student in students]
        delete_student_list = MyCombobox(self.canvas, values=student_names, width=45)
        delete_student_list.set("Pasirinkite ")
        delete_button = MyRButton(self.canvas, text="Pašalinti",
                                  command=lambda: self.confirm_delete_student(delete_student_list.get(), delete_student_list))

        student_label.place(x=85, y=10)
        line.place(x=25, y=35)
        self.label_info.place(x=30, y=55)
        delete_student_list.place(x=30, y=125)
        delete_button.place(x=145, y=165)

    def confirm_delete_student(self, selected_student, delete_student_list):
        if selected_student != "Pasirinkite ":
            confirmation = messagebox.askokcancel("Dėmesio", f"Ar tikrai norite pašalinti studentą: {selected_student}?")
            if confirmation:
                self.delete_student(selected_student, delete_student_list)
        else:
            messagebox.showwarning("Klaida", "Būtina pasirinkti studentą iš sąrašo.")

    def delete_student(self, selected_student, delete_student_list):
        student_to_delete = session.query(DuomenuBaze).filter_by(name=selected_student.split()[0],
                                                                 last_name=selected_student.split()[1]).first()

        if student_to_delete:
            session.delete(student_to_delete)
            session.commit()
            self.update_student_list_combobox(delete_student_list)

    def update_student_list_combobox(self, delete_student_list):
        students = session.query(DuomenuBaze).all()
        student_names = [f"{student.name} {student.last_name}" for student in students]
        delete_student_list['values'] = student_names
        delete_student_list.set("Pasirinkite ")
