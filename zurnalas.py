from sqlalchemy.orm import session, sessionmaker
from database import DuomenuBaze, MokomojiDalykoSkola, engine
from klases import  MyCombobox, MyLabel, MyEntry, MyCancelButton, MyRButton, MyText, ColumnValues
import tkinter as tk
from tkinter import messagebox, END
from sqlalchemy import extract, func

Session = sessionmaker(bind=engine)
session = Session()

class Zurnalas:
    def __init__(self, master):
        self.master = master
        self.canvas = master.canvas

    def add_canvas_elements_zurnalas(self):
        visi_studentai = session.query(DuomenuBaze).all()

        student_label = MyLabel(self.canvas, text="STUDENTŲ SĄRAŠAS")
        line = tk.Canvas(self.canvas, width=300, height=1, bg="white", highlightthickness=0)
        text_widget = MyText(self.canvas)

        student_label.place(x=90, y=10)
        line.place(x=25, y=35)
        text_widget.place(x=5, y=45)

        self.column_values = ColumnValues()
        columns = self.column_values.columns

        selected_column = MyCombobox(self.canvas, values=[display_name for attribute, display_name in columns])
        selected_column.set("Pasirinkite")
        selected_column.place(x=10, y=365)


        search_value_entry = MyEntry(self.canvas, width=15)
        search_value_entry.place(x=155, y=365)

        def on_cancel_button_click():
            self.add_canvas_elements_zurnalas()
        cancel_button = MyCancelButton(self.canvas, text='x', command=on_cancel_button_click)
        cancel_button.place(x=255, y=365)

        search_button = MyRButton(self.canvas, text="Ieškoti",
                                  command=lambda: self.perform_search(selected_column.get(), search_value_entry.get(),
                                                                      text_widget))
        search_button.place(x=285, y=360)

        text_widget.config(state=tk.NORMAL)
        for i, studentas in enumerate(visi_studentai, start=1):
            # Nustatome unikalų tag'ą kiekvienam studentui
            tag_name = f"student_{i}"
            bg_colors = ['#00211d', '#00423A', ]  # Dinamiškai generuojama spalva


            bg_color = bg_colors[i % len(bg_colors)]
            # Sukuriame tag'ą su nustatytais stiliais
            debts = session.query(MokomojiDalykoSkola).filter(MokomojiDalykoSkola.studentai.any(id=studentas.id)).all()
            debts_text = "Yra" if debts else "Nėra"
            text_widget.tag_configure(tag_name, background=bg_color, lmargin1=50, lmargin2=50, rmargin=10)
            text_widget.tag_configure("newline", background="#002A2E")
            # Įrašome studento informaciją su nustatytu tag'u
            text_widget.insert(tk.END, f"\n"
                                       f"{studentas.name.upper()} {studentas.last_name.upper()}\n"
                                       f"Studentas nuo: {studentas.student_since}\n"
                                       f"{studentas.division} Fakultetas: {studentas.study} \n"
                                       f"Skolos: {debts_text}\n"
                                       f"Priklauso tarybai: {studentas.member}\n"
                                       f"\n", tag_name)

            text_widget.insert(tk.END, "\n", "newline")

        text_widget.config(state=tk.DISABLED)

        def on_student_record_click(event, student_id):

            # Gauti studento informaciją pagal ID
            clicked_student = visi_studentai[student_id]


            new_canvas = tk.Canvas(self.master, width=340, height=325, bg="#00353B", highlightbackground="black",
                                   highlightthickness=0, )

            new_canvas.place(x=80, y=120)
            # Įdedame studento informaciją į Canvas
            new_canvas.create_text(75, 10, anchor="nw",
                                   text="Detali informacija",
                                   font=("Helvetica", 14, "bold"),
                                   fill='white')
            line = tk.Canvas(new_canvas, width=300, height=1, bg="white", highlightthickness=0)
            line.place(x=20, y=35)
            new_canvas.create_text(30, 50, anchor="nw",
                                   text=f"{clicked_student.name.upper()} {clicked_student.last_name.upper()}\n"
                                        f"\n"
                                        f"Gimimo data: {clicked_student.birth_date}\n"
                                        f"Studentas nuo: {clicked_student.student_since}\n"
                                        f"{clicked_student.division} Fakultetas: {clicked_student.study} \n"
                                        f"Priklauso tarybai: {clicked_student.member}\n"
                                        f"Slaptažodis: {clicked_student.password}\n",

                                   font=("Helvetica", 10),
                                   fill='white')
            new_canvas.create_text(30, 180, anchor="nw",
                                   text=

                                   f"Turimos skolos",

                                   font=("Helvetica", 12),
                                   fill='white')
            line_short = tk.Canvas(new_canvas, width=107, height=1, bg="white", highlightthickness=0)
            line_short.place(x=30, y=198)
            # Gauti studento skolas pagal ID
            debts = session.query(MokomojiDalykoSkola).filter(
                MokomojiDalykoSkola.studentai.any(id=clicked_student.id)).all()

            # Atvaizduoti skolas
            for i, debt in enumerate(debts, start=1):
                new_canvas.create_text(30, 185 + i * 20, anchor="nw",
                                       text=f"{debt.debt_name}",
                                       font=("Helvetica", 10),
                                       fill='white')
            close_button = MyCancelButton(new_canvas, text='x', command=new_canvas.destroy)
            close_button.place(x=318, y=3)

        # Pridėkite šį kodą cikle
        for i, studentas in enumerate(visi_studentai, start=1):
            tag_name = f"student_{i}"
            text_widget.tag_bind(tag_name, "<Button-1>",
                                 lambda event, student_id=i - 1: on_student_record_click(event, student_id))


    def perform_search(self, selected_column, search_value, text_widget):
        self.column_values = ColumnValues()
        columns = self.column_values.columns
        selected_attribute = next(attribute for attribute, display_name in columns if display_name == selected_column)

        if selected_attribute == 'student_since' and not search_value.isdigit():
            messagebox.showinfo("Klaida", "Galima įvesti tik skaičius, nurodykite tik metus ( pvz: 2018 ). ")
            return

        if selected_attribute == 'student_since':
            result = session.query(DuomenuBaze).filter(
                extract('year', getattr(DuomenuBaze, selected_attribute)) == int(search_value)).all()
        else:
            result = session.query(DuomenuBaze).filter(
                func.lower(getattr(DuomenuBaze, selected_attribute)).startswith(func.lower(search_value))).all()

        tag_name_base = "student_tag"
        bg_colors = ['#00211d', '#00423A']
        tag_names = []

        if result:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, END)  # isvalo esanti teksta

            for i, student in enumerate(result):
                bg_color = bg_colors[i % len(bg_colors)]
                tag_name = f"{tag_name_base}_{i}"
                tag_names.append(tag_name)
                text_widget.tag_configure("newline", background="#00272B")
                text_widget.tag_configure(tag_name, background=bg_color, lmargin1=50, lmargin2=50, rmargin=10)
                debts = session.query(MokomojiDalykoSkola).filter(
                    MokomojiDalykoSkola.studentai.any(id=student.id)).all()
                debts_text = "Yra" if debts else "Nėra"
                text_widget.insert(tk.END, f"\n"
                                           f"{student.name.upper()} {student.last_name.upper()}\n"
                                           f"Studentas nuo: {student.student_since}\n"
                                           f"{student.division} Fakultetas: {student.study} \n"
                                           f"Skolos: {debts_text}\n"
                                           f"Priklauso tarybai: {student.member}\n"
                                           f"\n", tag_name)

                text_widget.insert(tk.END, "\n", "newline")

            text_widget.config(state=tk.DISABLED)


        else:
            pass

        def on_record_click(event, student_id):
            clicked_student = result[student_id]

            new_canvas = tk.Canvas(self.master, width=340, height=325, bg="#00353B", highlightbackground="black",
                                   highlightthickness=0)
            line = tk.Canvas(new_canvas, width=300, height=1, bg="white", highlightthickness=0)
            line.place(x=20, y=35)
            new_canvas.place(x=80, y=120)
            new_canvas.create_text(75, 10, anchor="nw",
                                   text="Detali informacija",
                                   font=("Helvetica", 14, "bold"),
                                   fill='white')
            new_canvas.create_text(30, 50, anchor="nw",
                                   text=f"{clicked_student.name.upper()} {clicked_student.last_name.upper()}\n"
                                        f"\n"
                                        f"Gimimo data: {clicked_student.birth_date}\n"
                                        f"Studentas nuo: {clicked_student.student_since}\n"
                                        f"{clicked_student.division} Fakultetas: {clicked_student.study} \n"
                                        f"Priklauso tarybai: {clicked_student.member}\n"
                                        f"Slaptažodis: {clicked_student.password}\n",
                                   font=("Helvetica", 10),
                                   fill='white')
            new_canvas.create_text(30, 180, anchor="nw",
                                   text=

                                   f"Turimos skolos",

                                   font=("Helvetica", 12),
                                   fill='white')
            line_short = tk.Canvas(new_canvas, width=107, height=1, bg="white", highlightthickness=0)
            line_short.place(x=30, y=198)
            # Gauti studento skolas pagal ID
            debts = session.query(MokomojiDalykoSkola).filter(
                MokomojiDalykoSkola.studentai.any(id=clicked_student.id)).all()

            # Atvaizduoti skolas
            for i, debt in enumerate(debts, start=1):
                new_canvas.create_text(30, 185 + i * 20, anchor="nw",
                                       text=f"{debt.debt_name}",
                                       font=("Helvetica", 10),
                                       fill='white')
            close_button = MyCancelButton(new_canvas, text='x', command=new_canvas.destroy)
            close_button.place(x=318, y=3)

        for i, tag_name in enumerate(tag_names):
            text_widget.tag_bind(tag_name, "<Button-1>", lambda event, student_id=i: on_record_click(event, student_id))

        text_widget.config(state=tk.DISABLED)