from PIL import ImageTk, Image
import tkinter as tk
from klases import MyCanvas, MyButton
from tvarkyti import Tvarkyti
from ivesti import Ivesti
from pasalinti import  Pasalinti
from zurnalas import  Zurnalas


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Baigiamasis darbas")
        self.geometry("500x600")
        self.resizable(False, False)
        image_path = r"C:\Users\37067\PycharmProjects\pythonProject\PTU17\Baigiamasis\images\background.jpg"
        pillow_image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(pillow_image)

        background_label = tk.Label(self, image=background_image, )
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        background_label.image = background_image

        self.canvas = MyCanvas(self)
        self.canvas.pack(padx=10, pady=75)

        Zurnalas(self).add_canvas_elements_zurnalas()

        button1 = MyButton(self, text="Tvarkyti", command=self.tvarkyti_call, width=10)

        button2 = MyButton(self, text="Įvesti", command=self.ivesti_call, width=10)

        button3 = MyButton(self, text="Žurnalas", command=self.zurnalas_call, width=10)
        button4 = MyButton(self, text="Pašalinti", command=self.pasalinti_call, width=10)

        button1.place(x=75,  y=525)
        button2.place(x=165, y=525)
        button3.place(x=255, y=525)
        button4.place(x=345, y=525)
        self.status_bar = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor=tk.N)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def tvarkyti_call(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        Tvarkyti(self).add_canvas_elements_tvarkyti()

    def pasalinti_call(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        Pasalinti(self).add_canvas_elements_pasalinti()
    def zurnalas_call(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        Zurnalas(self).add_canvas_elements_zurnalas()

    def ivesti_call(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        Ivesti(self).add_canvas_elements_ivesti()


