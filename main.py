from PGTools import PGTools
from config import Configuration as cfg
from CSVTools import CSVTools
from Interpolation import *

PGTools = PGTools()
CSVTools = CSVTools()
Interpolation = Interpolation()

CSVTools.BakeDB(cfg.CSV_PATH)
Interpolation.rects = InterpolationRect.BuildRects(None, CSVTools.pointsArray)
PGTools.interpolationVisualiser.BuildRects(Interpolation.rects)

while True:
    PGTools.CheckEvents()
    PGTools.UpdateSurface()

    PGTools.CheckFPS()
