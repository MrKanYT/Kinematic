from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class SavesMenuWidget:

    mainLabel = None
    textLabel = None

    X = 5
    Y = 400
    WIDTH = 200
    HEIGHT = 195

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
                               text="<SaveMenu>",
                               font="Arial 14",
                               height=1,
                               bg=cfg.SUBCOLOR,
                               fg=cfg.TEXT_COLOR,
                               width=10
                               )

        self.textLabel.place(x=self.X+43, y=self.Y)





