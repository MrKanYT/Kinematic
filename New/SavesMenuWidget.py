from tkinter import *
from tkinter import ttk
from config import Cfg as cfg



class SavesMenuWidget:

    mainLabel = None

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=165, width=200)
        self.mainLabel.place(x=5, y=30)




