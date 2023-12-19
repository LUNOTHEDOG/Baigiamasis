
from tkinter import ttk
import tkinter as tk

from customtkinter import *

class MyCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)     # 3f4f4f

        combostyle = ttk.Style()

        
        if 'combostyle' not in combostyle.theme_names():
            combostyle.theme_create('combostyle', parent='alt',
                            settings = {'TCombobox':
                                        {'configure':
                                         {'selectbackground': '#151755',
                                          'fieldbackground': '#3f424f',
                                          'background': '#3f3f3f',
                                          'foreground': 'white',
                                          'bordercolor': 'black',
                                          'arrowcolor': 'white'
                                          },
                                         'map':
                                             {'background': [('active', '#151755'), ('disabled', '#3f424f')]
                                              }
                                         }}
                            )
            combostyle.theme_use('combostyle')
        self.configure(state="readonly", cursor='top_left_arrow')


class MyButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
       
        self.config(bg="#3f424f", fg="white")

        
        if hasattr(self.master, 'status_bar'):
            text = ""
            if self.cget('text') == "Žurnalas":
                text = "Studentų sąrašas"
            elif self.cget('text') == "Įvesti":
                text = "Sukurti naują studento įrašą"
            elif self.cget('text') == "Tvarkyti":
                text = "Tvarkyti esamus studentų įrašus"
            elif self.cget('text') == "Pašalinti":
                text = "Pašalinti studentą iš sistemos"

            self.master.status_bar.config(text=text)
    def on_leave(self, event):
        
        self.config(bg="SystemButtonFace", fg="black")

        
        if hasattr(self.master, 'status_bar'):
            self.master.status_bar.config(text="")
class MyCancelButton(CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=5, height=20, fg_color='#881347', hover_color='#151755', font=("Arial", 10, "bold"))
    def on_button_click(self):
        print("Mygtukas paspaustas!")

class MyRButton(CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=50, height=30, fg_color='#3f424f', hover_color='#151755')

class MySButton(CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=45, height=10, fg_color='#3f424f', hover_color='#151755')



class MyCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=350, height=400,bg="#00272B",  highlightbackground="white", highlightthickness=0)

class MyLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#00272B", fg="white", font=("Helvetica", 12, "bold"))




class MyLabelIvesti(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#00272B", fg="white", font=("Helvetica", 8, 'bold'))

class MyLabelTvarkyti(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#00353B", fg="white", font=("Helvetica", 8, 'bold'))


class MyEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        
        style = ttk.Style()
        self.configure(style="MyCustom.TEntry",font=("Helvetica", 8, "bold"))
        style.configure("MyCustom.TEntry", padding=0, relief="flat",  borderwidth=0, fieldbackground="#3f424f",
                        foreground="white")




class MyText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure( wrap="word", height=20, width=56, bg="#00272B",  bd=0, relief="flat", fg='white',
                        font=("Franklin Gothic Medium", 8))
        self.config(cursor="plus")




class ColumnValues:
    columns = [('name', 'Vardas'), ('last_name', 'Pavardė'),
               ('student_since', 'Studentas nuo'), ('division', 'Padalinys'), ('study', 'Studijos'),
                ('member', 'Tarybos narys')
               ]


class DivisionValues:
    division_choices = [
            "Informatikos",
            "Ekonomikos",
            "Teisės",
            "Biologijos",
            "Chemijos",
            "Architektūros",
            "Medicinos",
            "Matematikos ir statistikos"
        ]

class StudyValues:
    study_choices = [
        "Diskrečioji matematika",
        "Teorija skaičių",
        "Statistika",
        "Diferencialinės lygtys",
        "Aibės teorija",
        "Anatomija",
        "Fiziologija",
        "Farmakologija",
        "Chirurgija",
        "Pediatrija",
        "Architektūrinis dizainas",
        "Statybos technologijos",
        "Urbanistika",
        "Istorija ir teorija",
        "Kompiuterinis projektavimas",
        "Organinė chemija",
        "Neorganinė chemija",
        "Fizikinė chemija",
        "Analitinė chemija",
        "Biochemija",
        "Molekulinė biologija",
        "Ekologija",
        "Genetika",
        "Anatomija",
        "Botanika",
        "Civilinė teisė",
        "Kriminalinė teisė",
        "Tarptautinė teisė",
        "Teisės istorija",
        "Programavimas",
        "Duomenų bazių valdymas",
        "Tinklai ir komunikacija",
        "Operacinės sistemos"
    ]
