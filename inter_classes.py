import pygame as pg
from math import *

class Rect(pg.sprite.Sprite):
    def __init__(self, points):
        pg.sprite.Sprite.__init__(self)
        self.size_x = points[0].x - points[2].x
        self.points = points
        self.size_y = points[1].y - points[0].y
        self.image = pg.Surface((self.size_x, self.size_y))
        self.image.fill((255, 255, 255))                        #класс квадрата на рабочем поле
        self.rect = self.image.get_rect()
        self.rect.x = points[2].x
        self.rect.y = points[2].y

    def GetPoints(self, var):
        points = [
            [self.points[0].x, self.points[0].y, self.points[0].vars[0][var]],
            [self.points[1].x, self.points[1].y, self.points[1].vars[0][var]],              #получение точек квадрата в нужно порядке
            [self.points[2].x, self.points[2].y, self.points[2].vars[0][var]],
            [self.points[3].x, self.points[3].y, self.points[3].vars[0][var]]
        ]
        return points

class OutPoint(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.rotA = 0
        self.rotB = 0
        self.rotC = 0
        self.rotD = 0
        self.rotE = 0
        self.rotF = 0
        self.old_rotF = 0


class MousePoint(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.size = 1
        self.x = pg.mouse.get_pos()[0]
        self.y = pg.mouse.get_pos()[1]
        self.image = pg.Surface((1, 1))
        self.rect = self.image.get_rect()                               #точка, для которой расчитываются координаты
        self.rect.center = (self.x, self.y)

    def GetRect(self, objectsGroup):
        hits = pg.sprite.spritecollide(self, objectsGroup, False)
        try:
            return hits[0]                                              #получение квадрата, в котором находится точка
        except:
            return None

class CircleControlPoint(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.size = 5
        self.image = pg.Surface((self.size, self.size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()                               #точка, для которой расчитываются координаты
        self.rect.center = (750, 175)

    def GetRect(self, objectsGroup):
        hits = pg.sprite.spritecollide(self, objectsGroup, False)
        try:
            return hits[0]                                              #получение квадрата, в котором находится точка
        except:
            return None

class InterpolControlPoint(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.size = 5
        self.image = pg.Surface((self.size, self.size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()                               #точка, для которой расчитываются координаты
        self.rect.center = (250, 175)

    def GetRect(self, objectsGroup):
        hits = pg.sprite.spritecollide(self, objectsGroup, False)
        try:
            return hits[0]                                              #получение квадрата, в котором находится точка
        except:
            return None

class InputCircle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.x = 700
        self.y = 175
        self.size = 250
        self.image = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.size / 2
        self.rect.y = self.y - self.size / 2
        self.angle = self.GetDegToPoint((750, 175))

    def GetPosInRad(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def GetDegToPoint(self, pos):
        vector = pg.math.Vector2()
        deg = round(vector.angle_to(pg.math.Vector2(self.x, self.y) - pg.math.Vector2(pos[0], pos[1]))) + 180
        return deg

    def GetDistToPoint(self, pos):
        dist = round(hypot(pos[0], pos[1]))
        return dist

class InputCircleCenter(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.size / 2
        self.rect.y = self.y - self.size / 2

