import pygame as pg
from config import cfg
from inter_classes import *

class PgTools:
    def __init__(self, pressed = False):
        pg.init()
        self.screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        self.clock = pg.time.Clock()                                             # запуск pygame
        pg.display.set_caption(cfg.TITLE)
        self.display_surface = pg.display.get_surface()
        self.display_surface.blit(pg.transform.flip(self.display_surface, False, True), dest=(0, 0))

        self.allSprites = pg.sprite.Group()

        self.circleControlPoint = CircleControlPoint()
        self.interpolControlPoint = InterpolControlPoint()
        self.outPointGroup = pg.sprite.Group()

        self.outPoint = OutPoint()

        self.mousePoint = MousePoint()

        self.outPointGroup.add(self.circleControlPoint,
                          self.interpolControlPoint)  # добавляем точку, для которой считаем значения, в группу

        self.oldRect = None

        self.pressed = pressed

        self.handWorkspaceRecorder = self.HandWorkspaceRecorder()
        self.handVisualiser = self.HandVisualiser()

    def AddRectsToGroup(self, rects):
        for rect in rects:
            self.allSprites.add(rect)  # добавляем все квадраты в одну группу спрайтов

    def DrawText(self, surf, text, size, x, y):
        font = pg.font.Font(pg.font.match_font('arial'), size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()                             #функция вывода текста на экран
        text_rect.topleft = (x, y)
        surf.blit(text_surface, text_rect)

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

    class ControlCircle:
        def __init__(self):
            self.input_circle_group = pg.sprite.Group()
            self.input_circle = InputCircle()
            self.input_circle_group.add(self.input_circle)
            self.input_circle_group.add(InputCircleCenter(self.input_circle.x, self.input_circle.y))



