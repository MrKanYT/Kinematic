from tkinter import *
from tkinter import ttk
from config import Cfg as cfg



class HandVisualisationWidget:

    mainLabel = None
    textLabel = None

    X = 5
    Y = 600
    WIDTH = 505
    HEIGHT = 295

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            text="<HandVisualisation>",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.textLabel.place(x=self.X + 155, y=self.Y)




