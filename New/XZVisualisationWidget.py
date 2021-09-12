from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class XZVisualisationWidget:

    mainLabel = None
    textLabel = None

    X = 210
    Y = 315
    WIDTH = 300
    HEIGHT = 280

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            text="<XZVisualisation>",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.textLabel.place(x=self.X + 60, y=self.Y)



