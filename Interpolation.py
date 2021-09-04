class Interpolation:
    rects = ()


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

    class Point:
        x = None
        y = None
        vars = (None, None)

        def __init__(self, x=0, y=0, vars=(0, 0)):
            self.x = x
            self.y = y
            self.vars = vars


