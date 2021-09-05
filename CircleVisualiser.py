import pygame as pg
from math import *

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return out

class CircleVisualiser:

    output = None

    surface = None
    global_pos = []
    global_size = []

    circle = None
    point = None

    interpolation = None

    interpolation_x = ()

    def __init__(self, surface, pos, size, output):

        self.output = output

        self.surface = surface
        self.global_pos = pos
        self.global_size = size

        circle_pos_x = self.global_pos[0] + self.global_size[0] / 2
        circle_pos_y = self.global_pos[1] + self.global_size[1] / 2

        self.circle = self.Circle(self.surface, (circle_pos_x, circle_pos_y), self.global_size[1] / 2)

        self.point = self.Point(surface, (self.circle.global_pos[0] + 50, self.circle.global_pos[1]))


    def Update(self):
        self.circle.Draw()
        self.point.Draw()
        pg.draw.circle(self.surface, (255, 0, 0),self.circle.global_pos, 5)


    def SetPointFromGlobal(self, global_pos):
        angle = self.CalculateAngle(global_pos)
        self.point.global_pos = global_pos
        self.point.angle = angle

    def SetPointFromDistance(self, dist):
        self.point.distance = round(remap(dist, self.interpolation_x[0], self.interpolation_x[1], 0, self.circle.radius))
        self.point.global_pos = (self.circle.global_pos[0] + (self.point.distance * cos(self.point.angle)),
                                 self.circle.global_pos[1] + (self.point.distance * sin(self.point.angle)))

    def CalculateAngle(self, pos):
        vector = pg.math.Vector2()
        angle = round(vector.angle_to( pg.math.Vector2(pos[0], pos[1]) - pg.math.Vector2(self.circle.global_pos[0], self.circle.global_pos[1]))) + 180
        return angle

    def CalculateDistance(self):
        dist = round(hypot(self.point.global_pos[0] - self.circle.global_pos[0], self.point.global_pos[1] - self.circle.global_pos[1]))
        dist = remap(dist, 0, self.circle.radius, self.interpolation_x[0], self.interpolation_x[1])
        return dist

    def Calculate(self):
        self.output.A = self.point.angle




    class Circle():
        global_pos = []
        radius = 0
        surface = None

        def __init__(self, surface, global_pos, radius):
            self.surface = surface
            self.global_pos = global_pos
            self.radius = radius

        def Draw(self):
            pg.draw.circle(self.surface, (255, 255, 255), self.global_pos, self.radius)


    class Point():

        surface = None
        global_pos = []
        radius = 3

        angle = 0
        distance = 0

        def __init__(self, surface, global_pos):
            self.surface = surface
            self.global_pos = global_pos

        def Draw(self):
            pg.draw.circle(self.surface, (0, 0, 255), self.global_pos, self.radius)







