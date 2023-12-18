from sqlalchemy.orm import session, sessionmaker
import locale
from datetime import datetime
from tkcalendar import DateEntry
from database import DuomenuBaze, studentai_skolos, MokomojiDalykoSkola, engine
from klases import (MyButton, MyCombobox, MyLabel, MyEntry, MyCancelButton, MyRButton,
                     DivisionValues, StudyValues, MyLabelTvarkyti, MySButton)
import tkinter as tk
from tkinter import ttk, messagebox

Session = sessionmaker(bind=engine)
session = Session()


class Tvarkyti:
    def __init__(self, master):
        self.master = master
        self.canvas = master.canvas

    def add_canvas_elements_tvarkyti(self):
        main_label = MyLabel(self.canvas, text="STUDENTO DUOMENŲ TVARKYMAS")
        line = tk.Canvas(self.canvas, width=300, height=1, bg="white", highlightthickness=0)
        label_info_text = "Pasirinkite kurią informaciją norite tvarkyti"
        label_info = tk.Label(self.canvas, text=label_info_text, wraplength=240, justify="left",
                              bg="#00272B", fg="white", font=("Helvetica", 10), width=50, anchor="w")

        # Mygtukai
        personal_info_button = MyButton(self.canvas, text="PAGRINDINĖ INFORMACIJA",
                                        command=self.asmenine_informacija_call, width=25)

        debts_button = MyButton(self.canvas, text="STUDENTO SKOLOS", command=self.skolos_call, width=25)

        main_label.place(x=30, y=10)
        line.place(x=25, y=35)
        label_info.place(x=50, y=125)
        personal_info_button.place(x=85, y=170)
        debts_button.place(x=85, y=220)


    def asmenine_informacija_call(self):
        # Išvalyti seną canvas
        # self.clear_canvas()

        new_canvas = tk.Canvas(self.master, width=340, height=325, bg="#00353B", highlightbackground="black",
                               highlightthickness=0, )
        close_button = MyCancelButton(new_canvas, text='x', command=new_canvas.destroy)

        students = session.query(DuomenuBaze).all()
        student_combobox_values = [f"{student.name} {student.last_name}" for student in students]
        student_combobox_ids = [student.id for student in students]

        student_combobox = MyCombobox(new_canvas, values=student_combobox_values, width=30)
        student_combobox.set("Pasirinkite studentą")

        def patvirtinti_keitima_click():
            nonlocal student_combobox_ids
            name = self.name_entry.get().capitalize()
            last_name = self.last_name_entry.get().capitalize()
            birth_date = self.birth_entry.get()
            student_since = self.student_since_entry.get()
            division = self.division_entry.get()
            study = self.study_entry.get()
            member = self.member_entry.get()
            password = self.password_entry.get()

            if not all([name, last_name, birth_date, student_since, division, study, member, password]):
                tk.messagebox.showerror("Klaida", "Visi laukai turi būti užpildyti!")
                return

            selected_student_id = student_combobox_ids[student_combobox.current()]

            selected_student_obj = session.query(DuomenuBaze).filter_by(id=selected_student_id).first()

            selected_student_obj.name = name
            selected_student_obj.last_name = last_name
            selected_student_obj.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            selected_student_obj.student_since = datetime.strptime(student_since, "%Y-%m-%d").date()
            selected_student_obj.division = division
            selected_student_obj.study = study
            selected_student_obj.member = member
            selected_student_obj.password = password

            session.commit()

            students = session.query(DuomenuBaze).all()
            student_combobox_values = [f"{student.name} {student.last_name}" for student in students]
            student_combobox_ids = [student.id for student in students]
            student_combobox['values'] = student_combobox_values

            student_combobox.set("")
            student_combobox.set(f"{name} {last_name}")

            tk.messagebox.showinfo("Informacija", "Duomenys atnaujinti sėkmingai!")

        def fill_entry_fields(event):
            nonlocal student_combobox_ids
            selected_student_id = student_combobox_ids[student_combobox.current()]

            selected_student_obj = session.query(DuomenuBaze).filter_by(id=selected_student_id).first()

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_student_obj.name)

            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, selected_student_obj.last_name)

            self.birth_entry.delete(0, tk.END)
            self.birth_entry.insert(0, selected_student_obj.birth_date.strftime("%Y-%m-%d"))

            self.student_since_entry.delete(0, tk.END)
            self.student_since_entry.insert(0, selected_student_obj.student_since.strftime("%Y-%m-%d"))

            self.division_entry.set(selected_student_obj.division)
            self.study_entry.set(selected_student_obj.study)
            self.member_entry.set(selected_student_obj.member)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, selected_student_obj.password)

        student_combobox.bind("<<ComboboxSelected>>", fill_entry_fields)

        close_button.place(x=318, y=3)
        student_combobox.place(x=75, y=30)
        new_canvas.place(x=80, y=120)

        locale.setlocale(locale.LC_TIME, 'eu')
        name_label = MyLabelTvarkyti(new_canvas, text="VARDAS")
        last_name_label = MyLabelTvarkyti(new_canvas, text="PAVARDĖ")
        birth_label = MyLabelTvarkyti(new_canvas, text="GIMIMO DATA", bg="red")
        student_since_label = MyLabelTvarkyti(new_canvas, text="STUDENTAS NUO")
        division_label = MyLabelTvarkyti(new_canvas, text="PADALINYS")
        study_label = MyLabelTvarkyti(new_canvas, text="STUDIJOS")
        member_label = MyLabelTvarkyti(new_canvas, text="TARYBOS NARYS")
        password_label = MyLabelTvarkyti(new_canvas, text="SLAPTAŽODIS")

        self.name_entry = MyEntry(new_canvas, width=20)
        self.last_name_entry = MyEntry(new_canvas, width=20)
        self.birth_entry = DateEntry(new_canvas, selectmode='day', width=18, background='#3f4f4f',
                                     selectforeground='white',
                                     selectbackground='#3f4f4f', foreground='white', date_pattern='yyyy-mm-dd',
                                     borderwidth=2, cursor='top_left_arrow')
        self.birth_entry.bind("<Key>", self.disable_keyboard_input)
        selected_date = self.birth_entry.get_date()
        self.formatted_date = selected_date.strftime("%Y-%m-%d")
        print(f"Selected Date: {self.formatted_date}")
        self.student_since_entry = DateEntry(new_canvas, selectmode='day', width=18, background='#3f4f4f',
                                             selectforeground='white',
                                             selectbackground='#3f4f4f', foreground='white', date_pattern='yyyy-mm-dd',
                                             borderwidth=2, cursor='top_left_arrow')
        self.student_since_entry.bind("<Key>", self.disable_keyboard_input)
        selected_date_student_since = self.student_since_entry.get_date()
        self.formatted_date_student_since = selected_date_student_since.strftime("%Y-%m-%d")
        print(f"studentas nuo {self.formatted_date_student_since}")
        self.division_entry = MyCombobox(new_canvas, values=DivisionValues.division_choices, width=18)
        self.study_entry = MyCombobox(new_canvas, values=StudyValues.study_choices, width=18)
        self.member_entry = MyCombobox(new_canvas, values=['Taip', 'Ne'], width=18)
        self.password_entry = MyEntry(new_canvas, width=20)
        patvirtinti_button = MyRButton(new_canvas, text="Patvirtinti", command=patvirtinti_keitima_click)

        name_label.place(x=50, y=75)
        last_name_label.place(x=50, y=100)
        birth_label.place(x=50, y=125)
        student_since_label.place(x=50, y=150)
        division_label.place(x=50, y=175)
        study_label.place(x=50, y=200)
        member_label.place(x=50, y=225)
        password_label.place(x=50, y=250)
        self.name_entry.place(x=160, y=75)
        self.last_name_entry.place(x=160, y=100)
        self.birth_entry.place(x=160, y=125)
        self.student_since_entry.place(x=160, y=150)
        self.division_entry.place(x=160, y=175)
        self.study_entry.place(x=160, y=200)
        self.member_entry.place(x=160, y=225)
        self.password_entry.place(x=160, y=250)
        patvirtinti_button.place(x=160, y=275)


    def skolos_call(self):
        label_info_text = "TURIMOS SKOLOS"

        new_canvas = tk.Canvas( width=340, height=325, bg="#00353B", highlightbackground="black",
                               highlightthickness=0, )
        new_canvas.place(x=80, y=120)
        close_button = MyCancelButton(new_canvas, text='x', command=new_canvas.destroy)
        close_button.place(x=318, y=3)
        label_info = tk.Label(new_canvas, text=label_info_text,
                              bg="#00353B", fg="white", font=("Helvetica", 10, 'bold'))

        label_info.place(x=105, y=70)

        students = session.query(DuomenuBaze).all()

        student_combobox_values = [f"{student.name} {student.last_name}" for student in students]
        student_combobox_ids = [student.id for student in students]

        student_combobox = MyCombobox(new_canvas, values=student_combobox_values, width=30)
        student_combobox.set("Pasirinkite studentą")
        student_combobox.place(x=75, y=30)

        skolos_info_text = tk.Text(new_canvas, wrap=tk.WORD, width=30, height=7, font=("Helvetica", 10))
        skolos_info_text.config(state=tk.DISABLED, fg="white", bg="#00353B")
        skolos_info_text.place(x=64, y=100)

        skolos_combobox = ttk.Combobox(new_canvas, width=20)
        skolos_combobox.set("Pasirinkite skolą")
        skolos_combobox.place(x=50, y=250)

        def get_skolos_values():
            #visos skolos is MokomojiDalykoSkola lenteles
            skolos = session.query(MokomojiDalykoSkola).all()

            # Sugeneruoja skolas is skolu pavadinimu
            skolos_values = [skola.debt_name for skola in skolos]

            return skolos_values

        prideti_skola_combobox = MyCombobox(new_canvas, width=20)
        prideti_skola_combobox['values'] = get_skolos_values()
        prideti_skola_combobox.set("Pasirinkite skolą")
        prideti_skola_combobox.place(x=50, y=280)

        def update_skolos_info_text(*args):

            selected_student_index = student_combobox.current()
            selected_student = students[selected_student_index]

            # Tikrina, ar studentas turi skolu
            if not selected_student.skolos:
                skolos_info_text.config(state=tk.NORMAL)
                skolos_info_text.delete("1.0", tk.END)
                skolos_info_text.insert("1.0", "Šis studentas neturi skolų.")
                skolos_info_text.config(state=tk.DISABLED)
                return

            # Update skolos_info_text with student's debts
            skolos_info_text.config(state=tk.NORMAL)
            debts_info = "\n".join([f"{debt.debt_name}" for debt in selected_student.skolos])
            skolos_info_text.delete("1.0", tk.END)
            skolos_info_text.insert("1.0", debts_info)
            skolos_info_text.config(state=tk.DISABLED)


        def update_skolos_combobox():
            selected_student_id = student_combobox_ids[student_combobox.current()]
            selected_student = session.query(DuomenuBaze).get(selected_student_id)


            skolos_combobox_values = [skola.debt_name for skola in selected_student.skolos]
            skolos_combobox['values'] = skolos_combobox_values

        def on_combobox_selected(*args):
            update_skolos_combobox()
            update_skolos_info_text()

        student_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

        def remove_skola():
            selected_student_id = student_combobox_ids[student_combobox.current()]
            selected_student = session.query(DuomenuBaze).get(selected_student_id)

            selected_skola_name = skolos_combobox.get()

            # Patikrina, ar pasirinkta skolos reiksme
            if not selected_skola_name or selected_skola_name == "Pasirinkite skolą":
                tk.messagebox.showwarning("Klaida", "Nepasirinkta skola")
            else:
                selected_skola = session.query(MokomojiDalykoSkola).filter_by(debt_name=selected_skola_name).first()

                if selected_skola:

                    selected_student.skolos.remove(selected_skola)
                    session.commit()


                    update_skolos_combobox()
                    update_skolos_info_text()

                    tk.messagebox.showinfo("Informacija", f"Skola '{selected_skola_name}' panaikinta sėkmingai!")

        def add_new_skola():
            # Gauk pasirinktą studentą
            selected_student_id = student_combobox_ids[student_combobox.current()]
            selected_student = session.query(DuomenuBaze).get(selected_student_id)

            # Gauna pasirinkta skola is cobobox
            selected_skola_name = prideti_skola_combobox.get()  # Pavyzdžiui, pirmasis skolos Combobox

            # Tikrina ar pasirinkta skolos reiksme
            if not selected_skola_name or selected_skola_name == "Pasirinkite skolą":
                tk.messagebox.showwarning("Klaida", "Nepasirinkta skola")
            else:
                selected_skola = session.query(MokomojiDalykoSkola).filter_by(debt_name=selected_skola_name).first()

                # Tikrina ar studentas jau turi pasirinkta skola
                if selected_skola in selected_student.skolos:
                    tk.messagebox.showwarning("Klaida",
                                              f"Skola '{selected_skola_name}' jau yra pasirinkta šiam studentui!")
                else:
                    # Sukuria nauja skola
                    studentai_skolos_entry = {
                        'studentas_id': selected_student.id,
                        'mok_dalyko_skola_id': selected_skola.id
                    }

                    # Prideda irasa i tarpine lentele
                    session.execute(studentai_skolos.insert().values(studentai_skolos_entry))
                    session.commit()

                    # Atnaujina reiksmes
                    update_skolos_combobox()
                    update_skolos_info_text()

                    tk.messagebox.showinfo("Informacija", f"Skola '{selected_skola_name}' pridėta sėkmingai!")

        remove_skola_button = MySButton(new_canvas, text="Naikinti skolą", command=remove_skola)
        remove_skola_button.place(x=200, y=250)

        prideti_skola_button = MySButton(new_canvas, text="Sukurti skolą", command=add_new_skola)
        prideti_skola_button.place(x=200, y=280)

    def disable_keyboard_input(self, event):
        return "break"