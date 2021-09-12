from tkinter import *
from tkinter import ttk
from config import Cfg as cfg


class TimelineWidget:

    mainLabel = None
    textLabel = None

    X = 515
    Y = 735
    WIDTH = 800
    HEIGHT = 160

    def __init__(self):

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)

        self.textLabel = Label(
            text="<Timeline>",
            font="Arial 14",
            height=1,
            bg=cfg.SUBCOLOR,
            fg=cfg.TEXT_COLOR,
        )
        self.textLabel.place(x=self.X + 350, y=self.Y)




