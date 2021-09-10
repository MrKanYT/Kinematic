from tkinter import *
from config import Cfg as cfg

class UpperStatusBar:

    mainLabel = None
    label = None
    bottomLine = None

    def __init__(self):

        self.mainLabel = Label(border=0, bg=cfg.MAIN_COLOR, height=1)
        self.mainLabel.pack(side=TOP, fill=BOTH)


        self.label = Label(master=self.mainLabel,
                           text="<Status>",
                           anchor="w",
                           padx=20,
                           font="Arial 14",
                           fg=cfg.TEXT_COLOR,
                           bg=cfg.MAIN_COLOR)

        

        self.label.pack(side=LEFT)



