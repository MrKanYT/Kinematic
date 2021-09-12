from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class MatplotlibWidget:

    mainLabel = None
    textLabel = None

    X = 515
    Y = 30
    WIDTH = 800
    HEIGHT = 700

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            text="<MatplotlibViewport>",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.textLabel.place(x=self.X + 310, y=self.Y)



