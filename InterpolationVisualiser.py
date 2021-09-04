import pygame as pg
from Interpolation import *

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out

class InterpolationVisualiser:

    surface = None
    interpolationRects = [None]
    point = None
    spritesGroup = pg.sprite.Group()
    pointGroup = pg.sprite.Group()

    global_pos = [0, 0]
    global_size = [0, 0]

    CSV = None

    def __init__(self, surface, pos, size):
        self.surface = surface
        self.global_pos = pos
        self.global_size = size
        self.point = self.Point((self.global_pos[0] + self.global_size[0] / 2,
                                 self.global_pos[1] + self.global_size[1] / 2))
        self.pointGroup.add(self.point)

    def BuildRects(self, interpolationRects):
        self.interpolationRects = interpolationRects

        for i in interpolationRects:
             to_global = self.ToGlobal(i)
             self.spritesGroup.add(self.Rect(i, to_global[0], to_global[1]))

    def Update(self):
        self.spritesGroup.draw(self.surface)
        self.pointGroup.draw(self.surface)

    def ToGlobal(self, rect):
        global_pos_x = round(remap(rect.points[2].x, self.CSV.min_X, self.CSV.max_X, self.global_pos[0], self.global_pos[0] + self.global_size[0]))
        global_pos_y = round(remap(rect.points[2].y, self.CSV.min_Y, self.CSV.max_Y, self.global_pos[1], self.global_pos[1] + self.global_size[1]))

        global_second_pos_x = round(remap(rect.points[1].x, self.CSV.min_X, self.CSV.max_X, self.global_pos[0], self.global_pos[0] + self.global_size[0]))
        global_second_pos_y = round(remap(rect.points[1].y, self.CSV.min_Y, self.CSV.max_Y, self.global_pos[1], self.global_pos[1] + self.global_size[1]))

        global_size_x = global_second_pos_x - global_pos_x
        global_size_y = global_second_pos_y - global_pos_y

        return ((global_pos_x, global_pos_y), (global_size_x, global_size_y))

    def ToLocal(self, pos):
        local_pos_x = round(remap(pos[0], self.global_pos[0], self.global_pos[0] + self.global_size[0], self.CSV.min_X, self.CSV.max_X))
        local_pos_y = round(
            remap(pos[1], self.global_pos[1], self.global_pos[1] + self.global_size[1], self.CSV.min_Y, self.CSV.max_Y))
        return (local_pos_x, local_pos_y)

    def Calculate(self, output, rect):
        self.point.collide_rect = rect
        local = self.ToLocal(self.point.rect.center)
        out = (round(bilinear_interpolation(local[0], local[1], self.point.collide_rect.interpolationRect.GetPoints(0))),
               round(bilinear_interpolation(local[0], local[1], self.point.collide_rect.interpolationRect.GetPoints(1))))
        output.B = out[0]
        output.C = out[1]

    class Rect(pg.sprite.Sprite):

        interpolationRect = None

        size = (0, 0)

        def __init__(self, interpolationRect, globalPos, globalSize):
            pg.sprite.Sprite.__init__(self)

            self.globalPos = globalPos
            self.globalSize = globalSize

            self.interpolationRect = interpolationRect
            self.image = pg.Surface((self.globalSize[0], self.globalSize[1]))
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.x = self.globalPos[0]
            self.rect.y = self.globalPos[1]

    class Point(pg.sprite.Sprite):
        collide_rect = None

        def __init__(self, start_pos):
            pg.sprite.Sprite.__init__(self)
            self.size = 5
            self.image = pg.Surface((self.size, self.size))
            self.image.fill((0, 0, 255))
            self.rect = self.image.get_rect()
            self.rect.center = start_pos

        def GetRect(self, objectsGroup):
            hits = pg.sprite.spritecollide(self, objectsGroup, False)
            try:
                self.collide_rect = hits[0]
                return hits[0]
            except:
                self.collide_rect = None
                return None