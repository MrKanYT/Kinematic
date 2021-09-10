from tkinter import *
from UpperStatusBar import UpperStatusBar
from SavesWidget import SavesWidget
from config import Cfg as cfg
from tkinter import ttk
from PIL import Image, ImageTk
from PointMenuWidget import PointMenuWidget
from HandVisualisationWidget import HandVisualisationWidget
from SavesMenuWidget import SavesMenuWidget

class Main:

    root = None
    style = None

    upperStatusBar = None
    savesWidget = None
    pointMenuWidget = None
    handVisualisationWidget = None
    savesMenuWidget = None

    def __init__(self):
        self.root = Tk()
        self.style = ttk.Style()

        borderImage = ImageTk.PhotoImage(Image.open("Images/RoundedImage.png"))
        self.style.element_create("RoundedFrame",
                     "image", borderImage,
                     border=16, sticky="nsew")
        self.style.layout("RoundedFrame",
                     [("RoundedFrame", {"sticky": "nsew"})])

        self.root.title(cfg.WINDOW_NAME)
        self.root.geometry(cfg.SIZE)
        self.root.resizable(width=False, height=False)

        self.root.configure(bg=cfg.MAIN_COLOR)

        self.upperStatusBar = UpperStatusBar()
        self.savesWidget = SavesWidget()
        self.pointMenuWidget = PointMenuWidget()
        self.handVisualisationWidget = HandVisualisationWidget()

        self.root.mainloop()


if __name__ == "__main__":
    main = Main()