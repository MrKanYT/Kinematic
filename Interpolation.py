class Interpolation:
    rects = ()

def bilinear_interpolation(x, y, points):
    points = sorted(points)
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')                 #функция интерполяции

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
            ) / ((x2 - x1) * (y2 - y1) + 0.0)


class InterpolationRect:
    points = ()

    def __init__(self, points):
        self.points = points

    def BuildRects(self, pointsArray):
        out_rects = []
        rect_points = [[], [], [], []]
        for row in range(len(pointsArray)):
            if row >= len(pointsArray) - 1:
                break
            for point in range(len(pointsArray[row])):
                try:
                    indexTest = pointsArray[row][point][1]
                    indexTest = pointsArray[row + 1][point][1]
                    indexTest = pointsArray[row + 1][point + 1][1]
                    indexTest = pointsArray[row][point + 1][1]
                except IndexError:
                    continue
                rect_points[0] = pointsArray[row][point + 1]
                rect_points[1] = pointsArray[row + 1][point + 1]
                rect_points[2] = pointsArray[row][point]
                rect_points[3] = pointsArray[row + 1][point]
                test_points = [InterpolationRect.Point(rect_points[0][0], rect_points[0][1], [rect_points[0][2]]),
                               InterpolationRect.Point(rect_points[1][0], rect_points[1][1], [rect_points[1][2]]),
                               InterpolationRect.Point(rect_points[2][0], rect_points[2][1], [rect_points[2][2]]),
                               InterpolationRect.Point(rect_points[3][0], rect_points[3][1], [rect_points[3][2]])]

                out_rects.append(InterpolationRect(test_points))
        return out_rects

    def GetPoints(self, var):
        points = [
            [self.points[0].x, self.points[0].y, self.points[0].vars[0][var]],
            [self.points[1].x, self.points[1].y, self.points[1].vars[0][var]],              #получение точек квадрата в нужно порядке
            [self.points[2].x, self.points[2].y, self.points[2].vars[0][var]],
            [self.points[3].x, self.points[3].y, self.points[3].vars[0][var]]
        ]
        return points

    class Point:
        x = None
        y = None
        vars = (None, None)

        def __init__(self, x=0, y=0, vars=(0, 0)):
            self.x = x
            self.y = y
            self.vars = vars


