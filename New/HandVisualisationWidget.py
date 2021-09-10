from tkinter import *
from tkinter import ttk
from config import Cfg as cfg



class HandVisualisationWidget:

    mainLabel = None

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=295, width=505)
        self.mainLabel.place(x=5, y=600)




