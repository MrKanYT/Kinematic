import pygame as pg
from config import cfg
from math import *

class PgTools:
    def __init__(self, pressed = False):
        pg.init()
        self.screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        self.clock = pg.time.Clock()                                             # запуск pygame
        pg.display.set_caption(cfg.TITLE)
        self.display_surface = pg.display.get_surface()
        self.display_surface.blit(pg.transform.flip(self.display_surface, False, True), dest=(0, 0))

        self.outPointGroup = pg.sprite.Group()



        self.mousePoint = self.MousePoint()

        self.outPointGroup.add(self.ControlCircle.circleControlPoint,
                          self.InterpolationVisualizer.interpolControlPoint)  # добавляем точку, для которой считаем значения, в группу

        self.pressed = pressed

        self.handWorkspaceRecorder = self.HandWorkspaceRecorder()
        self.handVisualiser = self.HandVisualiser()
        self.controlCircle = self.ControlCircle()
        self.interpolationVisualizer = self.InterpolationVisualizer()

    def UpdateScreen(self):
        self.screen.fill('gray')  # очищаем экран


    def DrawAllText(self):

        screen = self.screen
        self.DrawText(screen, f"Angle A: {round(self.outPoint.rotA)}", 30, 5, 50)
        self.DrawText(screen, f"Angle B: {round(self.outPoint.rotB)}", 30, 5, 100)
        self.DrawText(screen, f"Angle C: {round(self.outPoint.rotC)}", 30, 5, 150)
        self.DrawText(screen, f"Angle D: {round(self.outPoint.rotD)}", 30, 5, 200)
        self.DrawText(screen, f"Angle E: {round(self.outPoint.rotE)}", 30, 5, 250)
        self.DrawText(screen, f"Angle F: {round(self.outPoint.rotF)}", 30, 5, 300)

    def AddRectsToGroup(self, rects):
        for rect in rects:
            self.allSprites.add(rect)  # добавляем все квадраты в одну группу спрайтов

    def DrawText(self, surf, text, size, x, y):
        font = pg.font.Font(pg.font.match_font('arial'), size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()                             #функция вывода текста на экран
        text_rect.topleft = (x, y)
        surf.blit(text_surface, text_rect)

    class MousePoint(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.size = 1
            self.x = pg.mouse.get_pos()[0]
            self.y = pg.mouse.get_pos()[1]
            self.image = pg.Surface((1, 1))
            self.rect = self.image.get_rect()  # точка, для которой расчитываются координаты
            self.rect.center = (self.x, self.y)

        def GetRect(self, objectsGroup):
            hits = pg.sprite.spritecollide(self, objectsGroup, False)
            try:
                return hits[0]  # получение квадрата, в котором находится точка
            except:
                return None



    class HandWorkspaceRecorder:
        def __init__(self):
            self.Hand_record = False
            self.Hand_record_list = [99999, -99999, 99999, -99999]


    class HandVisualiser:
        shoulder_point = [0, 0]
        wrist_point = [0, 0]
        hand_point = [0, 0]
        end_point = [0, 0]

        shoulder_point_display = [0, 0]
        wrist_point_display = [0, 0]
        hand_point_display = [0, 0]
        end_point_display = [0, 0]

        def __init__(self):
            self.hand_input = self.HandInputPoint()

            self.hand_input.L1 = cfg.LENS["shoulder"]
            self.hand_input.L2 = cfg.LENS["wrist"]
            self.hand_input.L3 = cfg.LENS["hand"]

        def Visualise(self, screen):
            pg.draw.line(screen, [255, 0, 0], self.shoulder_point_display,
                         self.wrist_point_display, 3)
            pg.draw.line(screen, [0, 255, 0], self.wrist_point_display,
                         self.hand_point_display, 3)
            pg.draw.line(screen, [0, 0, 255], self.hand_point_display,
                         self.end_point_display, 3)

        def CalcPoints(self, L1, L2, L3, a1, a2, a3):
            L1 /= 2
            L2 /= 2
            L3 /= 2
            a1 /= -5
            a2 /= -5
            a3 /= -5
            self.wrist_point = [
                L1 * cos(a1), L1 * sin(a1),
            ]
            self.hand_point = [
                L1 * cos(a1) + L2 * cos(a2), L1 * sin(a1) + L2 * sin(a2),
            ]
            self.end_point = [
                L1 * cos(a1) + L2 * cos(a2) + L3 * cos(a3), L1 * sin(a1) + L2 * sin(a2) + L3 * sin(a3),
            ]

        def CalcDisplayPoints(self, startx, starty):
            self.shoulder_point_display[0] = self.shoulder_point[0] + startx
            self.shoulder_point_display[1] = self.shoulder_point[1] + starty

            self.wrist_point_display[0] = self.wrist_point[0] + startx
            self.wrist_point_display[1] = self.wrist_point[1] + starty

            self.hand_point_display[0] = self.hand_point[0] + startx
            self.hand_point_display[1] = self.hand_point[1] + starty

            self.end_point_display[0] = self.end_point[0] + startx
            self.end_point_display[1] = self.end_point[1] + starty

        class HandInputPoint:
            def __init__(self):
                self.x = 0
                self.y = 0
                self.z = 0
                self.a1 = 0
                self.a2 = 0
                self.a3 = 0
                self.L1 = 0
                self.L2 = 0
                self.L3 = 0
                self.rot = 0
                self.a4 = 0
                self.a5 = 0

    class ControlCircle(pg.sprite.Sprite):
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.circleControlPoint = self.CircleControlPoint()
            self.x = 700
            self.y = 175
            self.size = 250
            self.image = pg.Surface((self.size, self.size), pg.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = self.x - self.size / 2
            self.rect.y = self.y - self.size / 2
            self.angle = self.GetDegToPoint((750, 175))
            self.input_circle_group = pg.sprite.Group()
            self.input_circle_group.add(self)
            self.input_circle_group.add(self.InputCircleCenter(self.x, self.y))

        def Draw(self, screen):
            pg.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size / 2)
            self.input_circle_group.draw(screen)

        def GetPosInRad(self, pos):
            return (pos[0] - self.x, pos[1] - self.y)

        def GetDegToPoint(self, pos):
            return round(pg.math.Vector2().angle_to(pg.math.Vector2(self.x, self.y) - pg.math.Vector2(pos[0], pos[1]))) + 180

        def GetDistToPoint(self, pos):
            return round(hypot(pos[0], pos[1]))

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

        class CircleControlPoint(pg.sprite.Sprite):
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                self.size = 5
                self.image = pg.Surface((self.size, self.size))
                self.image.fill((0, 0, 255))
                self.rect = self.image.get_rect()  # точка, для которой расчитываются координаты
                self.rect.center = (750, 175)

            def GetRect(self, objectsGroup):
                hits = pg.sprite.spritecollide(self, objectsGroup, False)
                try:
                    return hits[0]  # получение квадрата, в котором находится точка
                except:
                    return None

    class InterpolationVisualizer:
        def __init__(self):
            self.allSprites = pg.sprite.Group()
            self.interpolControlPoint = self.InterpolControlPoint()

            self.oldRect = None

        def DrawAllRects(self, screen):
            self.allSprites.draw(screen)  # выводим на экран все квадраты

        class InterpolControlPoint(pg.sprite.Sprite):
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                self.size = 5
                self.image = pg.Surface((self.size, self.size))
                self.image.fill((0, 0, 255))
                self.rect = self.image.get_rect()  # точка, для которой расчитываются координаты
                self.rect.center = (250, 175)

            def GetRect(self, objectsGroup):
                hits = pg.sprite.spritecollide(self, objectsGroup, False)
                try:
                    return hits[0]  # получение квадрата, в котором находится точка
                except:
                    return None

        class Rect(pg.sprite.Sprite):
            def __init__(self, points):
                pg.sprite.Sprite.__init__(self)
                self.size_x = points[0].x - points[2].x
                self.points = points
                self.size_y = points[1].y - points[0].y
                self.image = pg.Surface((self.size_x, self.size_y))
                self.image.fill((255, 255, 255))  # класс квадрата на рабочем поле
                self.rect = self.image.get_rect()
                self.rect.x = points[2].x
                self.rect.y = points[2].y

            def GetPoints(self, var):
                points = [
                    [self.points[0].x, self.points[0].y, self.points[0].vars[0][var]],
                    [self.points[1].x, self.points[1].y, self.points[1].vars[0][var]],
                    # получение точек квадрата в нужно порядке
                    [self.points[2].x, self.points[2].y, self.points[2].vars[0][var]],
                    [self.points[3].x, self.points[3].y, self.points[3].vars[0][var]]
                ]
                return points




