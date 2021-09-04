from PGTools import PGTools
from config import Configuration as cfg
from CSVTools import CSVTools
from Interpolation import *
from Output import Output
import pygame as pg

PGTools = PGTools()
CSVTools = CSVTools()
Interpolation = Interpolation()


CSVTools.BakeDB(cfg.CSV_PATH)
Interpolation.rects = InterpolationRect.BuildRects(None, CSVTools.pointsArray)
PGTools.interpolationVisualiser.CSV = CSVTools
PGTools.interpolationVisualiser.BuildRects(Interpolation.rects)


while True:
    PGTools.CheckEvents()
    PGTools.UpdateSurface()

    PGTools.output.Draw()

    PGTools.interpolationVisualiser.Update()

    pg.display.flip()

    PGTools.CheckFPS()
