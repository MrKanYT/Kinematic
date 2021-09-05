import pygame as pg
from InterpolationVisualiser import InterpolationVisualiser
from Output import Output
from CircleVisualiser import CircleVisualiser
from math import *

class PGTools:

    screen = None
    clock = None
    surface = None

    interpolationVisualiser = None
    circleVisualiser = None

    width = None
    height = None

    output = None

    mousePoint = None

    def __init__(self, width=1600, height=900, window_name="Remote control", fps=60):
        # create main window
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        pg.display.set_caption(window_name)
        self.surface = pg.display.get_surface()
        self.fps = fps

        self.width = width
        self.height = height

        self.mousePoint = self.MousePoint()

        self.interpolation_padding = 20
        self.interpolationVisualiser = InterpolationVisualiser(self.surface, [self.interpolation_padding, self.interpolation_padding], [width/2 - self.interpolation_padding * 2, height/2 - self.interpolation_padding * 2])

        self.output_padding = 20
        self.output = Output(self.surface, [self.width / 2 + self.output_padding, self.height / 2 + self.output_padding])

        self.circle_padding = 20
        self.circleVisualiser = CircleVisualiser(self.surface, (self.width / 2 + self.circle_padding, 0 + self.circle_padding), (self.width / 2 - self.circle_padding * 2, self.height / 2 - self.circle_padding * 2), self.output)


    def UpdateSurface(self):
        line_width = 2

        #clear surface
        self.screen.fill('gray')

        # draw split lines
        pg.draw.line(self.surface, (150, 150, 150), (self.width / 2 - line_width / 2, 0), (self.width / 2 - line_width / 2, self.height), line_width)
        pg.draw.line(self.surface, (150, 150, 150), (0, self.height / 2 - line_width / 2),
                     (self.width, self.height / 2 - line_width / 2), line_width)

    def CheckFPS(self):
        self.clock.tick(self.fps)

    def CheckEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mousePoint.pressed = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.mousePoint.pressed = False


    def CheckCollide(self):
        if self.mousePoint.pressed:
            self.mousePoint.rect.center = pg.mouse.get_pos()
            _rect = self.mousePoint.GetRect(self.interpolationVisualiser.spritesGroup)
            if  _rect != None:
                self.interpolationVisualiser.point.rect.center = self.mousePoint.rect.center
                self.interpolationVisualiser.Calculate(self.output, _rect)
                self.circleVisualiser.SetPointFromDistance(self.interpolationVisualiser.ToLocal(self.interpolationVisualiser.point.rect.center)[0])
                return
            to_zero_x = self.mousePoint.rect.center[0] - self.circleVisualiser.circle.global_pos[0]
            to_zero_y = self.mousePoint.rect.center[1] - self.circleVisualiser.circle.global_pos[1]
            if round(hypot(to_zero_x, to_zero_y)) < self.circleVisualiser.circle.radius:
                self.circleVisualiser.SetPointFromGlobal(self.mousePoint.rect.center)
                self.interpolationVisualiser.point.rect.center = (self.interpolationVisualiser.PosToGlobal((self.circleVisualiser.CalculateDistance(), 0))[0], self.interpolationVisualiser.point.rect.center[1])
                _hit = self.interpolationVisualiser.point.GetRect(self.interpolationVisualiser.spritesGroup)
                print(_hit)
                if _hit != None:
                    self.interpolationVisualiser.Calculate(self.output, _hit)

    class MousePoint(pg.sprite.Sprite):
        pressed = False
        def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.size = 1
            self.x = pg.mouse.get_pos()[0]
            self.y = pg.mouse.get_pos()[1]
            self.image = pg.Surface((1, 1))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        def GetRect(self, objectsGroup):
            hits = pg.sprite.spritecollide(self, objectsGroup, False)
            try:
                return hits[0]
            except:
                return None





