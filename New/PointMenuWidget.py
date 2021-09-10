from tkinter import *
from tkinter import ttk
from config import Cfg as cfg

class PointMenuWidget:

    mainLabel = None

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=565, width=300)
        self.mainLabel.place(x=210, y=30)




