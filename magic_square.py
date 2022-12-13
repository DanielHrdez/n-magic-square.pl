# Importamos las librerías necesarias para la interfaz gráfica y cargar el archivo de prolog
from tkinter.constants import GROOVE, RAISED, RIDGE, RIGHT, X
from pyswip import Prolog
import tkinter as tk
import time
import os
import sys

# Constantes
FG_1 = "white"
FG_2 = "gray70"
BG_1 = "gray10"
BG_2 = "gray20"
BG_3 = "gray20"
BG_4 = "gray30"
BG_5 = "black"

MID = 0.5
DIM = 0.2

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Clase para la interfaz gráfica
class Magic_Square(tk.Tk):
    # Constructor
    def __init__(self, name="Example Title", width=620, height=480, prolog_file=None, query=None, icon=None):
        # Configuraciones de la interfaz gráfica
        super().__init__()
        self.title(name)
        self.iconbitmap(icon)
        self.geometry("{width}x{height}".format(width=width, height=height))
        self.resizable(True, True)
        self.config(bg=BG_1)
        self.bind('<Configure>', self.resize)
        self.bind('<Return>', self.submit)

        for i in range(10):
            self.bind("{}".format(i), self.text_entry)

        self.bind("<BackSpace>", self.text_entry)

        self.font = "Arial 16 bold"
        self.font_result = "Arial 16 bold"

        # Carga del archivo de prolog
        self.prolog = Prolog()
        if prolog_file:
            self.prolog.consult(prolog_file)

        self.n = tk.IntVar()
        self.n.set(3)

        self.next = tk.IntVar()

        aux = 0.1

        # Botones de la interfaz
        self.n_entry = tk.Entry(self, textvariable=self.n, width=3, bg=BG_2,
                                fg=FG_1, font=self.font, justify="center", borderwidth=0)
        self.n_entry.place(relx=MID-aux, rely=MID+aux*2,
                           anchor="center", relheight=DIM-aux, relwidth=DIM)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit,
                                     bg=BG_3, fg=FG_1, font=self.font, borderwidth=0, justify="center")
        self.submit_button.place(relx=MID+aux, rely=MID+aux*2,
                               anchor="center", relheight=DIM-aux, relwidth=DIM)

        self.next_button = tk.Button(self, text="Next", command=lambda: self.next.set(1),
                                    bg=BG_3, fg=FG_1, font=self.font, borderwidth=0, justify="center")

        self.submit_button.bind("<Enter>", self.on_enter)
        self.submit_button.bind("<Leave>", self.on_leave)
        self.next_button.bind("<Enter>", self.on_enter)
        self.next_button.bind("<Leave>", self.on_leave)

        self.result_table = tk.Frame(self, bg=BG_4)
        self.result_table.place(relx=MID, rely=MID-aux/2,
                                anchor="center", relheight=DIM*2, relwidth=DIM*2)

        self.entry_list = []
        self.query = query

    # Función para cambiar N con el teclado
    def text_entry(self, event):
        if event.char.isdigit() and self.focus_get() != self.n_entry:
            self.n_entry.insert(0, event.char)
        elif self.focus_get() != self.n_entry:
            self.n_entry.delete(0)

    # Función para hacer consulta de prolog
    def set_query(self, query):
        self.query = query

    # Función para cargar archivo de prolog
    def consult(self, file):
        self.prolog.consult(file)

    # Función para ejecutar el programa
    def submit(self, event=None):
        # check if submit button is visible
        if not self.submit_button.winfo_ismapped():
            self.next.set(1)
            return

        self.submit_button.place_forget()

        self.next_button.place(relx=MID+0.1, rely=MID+0.1*2,
                               anchor="center", relheight=DIM-0.1, relwidth=DIM)
                            
        n = self.n.get()
        t1 = time.time()

        # En cada iteración del resultado se guarda en una lista, se muestra el resultado y el tiempo de ejecución
        for result in self.prolog.query(self.query.format(n=n)):
            if self.n.get() != n:
                break
            if result:
                t2 = time.time()
                self.timer = tk.Label(self, text="Time: {:.2f}s".format(t2-t1), bg=BG_1, fg=FG_1, font="Arial 10 bold")
                self.timer.place(relx=0.85, rely=0.95,
                                 anchor="center", relheight=0.07, relwidth=0.3)
                self.result = result["Result"]
                self.display_result(n)
                t1 = time.time()
                
                self.wait_variable(self.next)

        self.next_button.place_forget()
        self.submit_button.place(relx=MID+0.1, rely=MID+0.1*2,
                                 anchor="center", relheight=DIM-0.1, relwidth=DIM)

    # Función para mostrar el resultado
    def display_result(self, n=None):
        self.entry_list = []

        for i in range(n):
            self.entry_list.append([])
            for j in range(n):
                self.entry_list[i].append(tk.Label(self.result_table, text=self.result[i][j], bg=BG_4, fg=FG_1,
                                                   font=self.font_result, highlightbackground=BG_3, highlightthickness=1))
                self.entry_list[i][j].place(relx=j/n + MID/n,
                                            rely=i/n + MID/n,
                                            anchor="center",
                                            relheight=1/n,
                                            relwidth=1/n)

    # Función para cambiar el tamaño de la fuente de la ventana
    def resize(self, event):
        height = self.winfo_height()
        width = self.winfo_width()
        size = min(height, width)/4
        self.font = "Arial {size} bold".format(size=int(size/6))

        self.n_entry.config(font=self.font)
        self.submit_button.config(font=self.font)
        self.next_button.config(font=self.font)

        self.font_result = "Arial {size} bold".format(size=int(size/(self.n.get()*2)))

        for i in range(min(self.n.get(), len(self.entry_list))):
            for j in range(self.n.get()):
                self.entry_list[i][j].config(font=self.font_result)

    # Función para cambiar el color del botón cuando se pasa el mouse por encima
    def on_enter(self, event):
        self.submit_button.config(bg=BG_5)
        self.next_button.config(bg=BG_5)

    # Función para cambiar el color del botón cuando se sale del mouse
    def on_leave(self, event):
        self.submit_button.config(bg=BG_3)
        self.next_button.config(bg=BG_3)

# Función principal que ejecuta un ejemplo de ejecución de la clase
def main():
    path = resource_path("magic_square/magic_square.pl")
    path = path.replace("\\", "/")
    icon = resource_path("prolog/prolog.ico")
    icon = icon.replace("\\", "/")
    mg = Magic_Square(name="Magic Square", prolog_file=path, icon=icon)
    mg.query = "magic_square({n}, Result)"
    mg.mainloop()
    mg.next.set(0)

if __name__ == "__main__":
    main()