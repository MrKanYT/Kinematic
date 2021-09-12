from tkinter import *
from tkinter import ttk
from config import Cfg as cfg



class SavesWidget:

    mainLabel = None
    textLabel = None

    X = 5
    Y = 30
    WIDTH = 200
    HEIGHT = 365

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", width=self.WIDTH, height=self.HEIGHT)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
                               text="<Saves>",
                               font="Arial 14",
                               height=1,
                               bg=cfg.SUBCOLOR,
                               fg=cfg.TEXT_COLOR,
                               )
        self.textLabel.place(x=self.X + 50, y=self.Y)






