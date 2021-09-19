from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
import Viewport3D


class MatplotlibWidget:

    root = None
    mainLabel = None

    viewport = None

    X = 515 * cfg.SIZE_MULT
    Y = 30 * cfg.SIZE_MULT
    WIDTH = 800 * cfg.SIZE_MULT
    HEIGHT = 700 * cfg.SIZE_MULT

    def __init__(self, root):
        self.root = root

        self.mainLabel = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainLabel.place(x=self.X, y=self.Y)
    '''
        Viewport3D.Build(self.mainLabel)

        self.root.bind("<KeyPress>", Viewport3D.point.changing_flags)'''






