from config import cfg
from inter_classes import *

class Interpolation:

    def to_pygame(self, coords):
        return cfg.HEIGHT - coords

    def bilinear_interpolation(self, x, y, points):
        points = sorted(points)
        (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

        if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
            raise ValueError('points do not form a rectangle')
        if not x1 <= x <= x2 or not y1 <= y <= y2:
            raise ValueError('(x, y) not within the rectangle')                 #функция интерполяции

        return (q11 * (x2 - x) * (self.to_pygame(y2) - self.to_pygame(y)) +
                q21 * (x - x1) * (self.to_pygame(y2) - self.to_pygame(y)) +
                q12 * (x2 - x) * (self.to_pygame(y) - self.to_pygame(y1)) +
                q22 * (x - x1) * (self.to_pygame(y) - self.to_pygame(y1))
               ) / ((x2 - x1) * (self.to_pygame(y2) - self.to_pygame(y1)) + 0.0)

    class Point:
        def __init__(self, x=0, y=0, vars=[0, 0]):
            self.x = x
            self.y = y
            self.vars = vars    #углы моторов

        x = 0                                  #класс точки
        y = 0

        vars = [0, 0]

    def build_rects(self, points):
        out_rects = []
        rect_points = [[], [], [], []]
        for row in range(len(points)):
            if row >= len(points)-1:
                break
            for point in range(len(points[row])):
                try:
                    indexTest = points[row][point][1]
                    indexTest = points[row + 1][point][1]
                    indexTest = points[row + 1][point + 1][1]
                    indexTest = points[row][point + 1][1]
                except IndexError:
                    continue                                            #получение одномерного массива квадратов из двумерного массива точек
                rect_points[0] = points[row][point + 1]
                rect_points[1] = points[row + 1][point + 1]
                rect_points[2] = points[row][point]
                rect_points[3] = points[row + 1][point]
                test_points = [self.Point(rect_points[0][0], rect_points[0][1], [rect_points[0][2]]),
                               self.Point(rect_points[1][0], rect_points[1][1], [rect_points[1][2]]),
                               self.Point(rect_points[2][0], rect_points[2][1], [rect_points[2][2]]),
                               self.Point(rect_points[3][0], rect_points[3][1], [rect_points[3][2]])]

                out_rects.append(Rect(test_points))
        self.Rects = out_rects

