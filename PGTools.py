import pygame as pg
from InterpolationVisualiser import InterpolationVisualiser

class PGTools:

    screen = None
    clock = None
    surface = None

    interpolationVisualiser = None

    def __init__(self, width=1600, height=900, window_name="Remote control", fps=60):
        # create main window
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        pg.display.set_caption(window_name)
        self.surface = pg.display.get_surface()
        self.fps = fps

        self.interpolationVisualiser = InterpolationVisualiser(self.surface)


    def UpdateSurface(self):
        #clear surface
        self.screen.fill('gray')

        # draw surface
        pg.display.flip()

    def CheckFPS(self):
        self.clock.tick(self.fps)

    def CheckEvents(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                exit()



