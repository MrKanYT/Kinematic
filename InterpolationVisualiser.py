import pygame as pg
from Interpolation import *

class InterpolationVisualiser:

    surface = None
    interpolationRects = [None]

    def __init__(self, surface):
        self.surface = surface

    def BuildRects(self, interpolationRects):
        self.interpolationRects = interpolationRects

        for i in interpolationRects:
            self.Rect(i)


    class Rect(pg.sprite.Sprite):

        interpolationRect = None

        size = (0, 0)

        def __init__(self, interpolationRect):
            pg.sprite.Sprite.__init__(self)

            self.interpolationRect = interpolationRect
            self.size = (interpolationRect.points[0].x - interpolationRect.points[2].x,
                         interpolationRect.points[1].y - interpolationRect.points[0].y)

            print(self.size)