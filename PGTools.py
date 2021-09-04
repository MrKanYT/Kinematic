import pygame as pg
from InterpolationVisualiser import InterpolationVisualiser
from Output import Output

class PGTools:

    screen = None
    clock = None
    surface = None

    interpolationVisualiser = None

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

        interpolation_padding = 20
        self.interpolationVisualiser = InterpolationVisualiser(self.surface, [interpolation_padding, interpolation_padding], [width/2 - interpolation_padding * 2, height/2 - interpolation_padding * 2])

        output_padding = 20
        self.output = Output(self.surface, [self.width / 2 + output_padding, self.height / 2 + output_padding])


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





