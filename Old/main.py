from PGTools import PGTools
from config import Configuration as cfg
from CSVTools import CSVTools
from Interpolation import *
import pygame as pg

PGTools = PGTools()
CSVTools = CSVTools()
Interpolation = Interpolation()


CSVTools.BakeDB(cfg.CSV_PATH)
Interpolation.rects = InterpolationRect.BuildRects(None, CSVTools.pointsArray)
PGTools.interpolationVisualiser.CSV = CSVTools
PGTools.interpolationVisualiser.BuildRects(Interpolation.rects)
PGTools.circleVisualiser.interpolation_x = (CSVTools.min_X, CSVTools.max_X)
PGTools.circleVisualiser.interpolation = PGTools.interpolationVisualiser


while True:
    PGTools.CheckEvents()
    PGTools.UpdateSurface()

    PGTools.CheckCollide()

    PGTools.interpolationVisualiser.Update()
    PGTools.circleVisualiser.Update()

    PGTools.circleVisualiser.Calculate()

    PGTools.output.Draw()

    pg.display.flip()

    PGTools.CheckFPS()
