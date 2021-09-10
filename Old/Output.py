import pygame as pg

class Output:
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0

    pos = ()
    font_size = 40
    line_spacing = 10

    font = None
    surface = None

    def __init__(self, surface, pos):

        self.font = pg.font.Font(pg.font.match_font('arial'), self.font_size)
        self.surface = surface
        self.pos = pos

    def Draw(self):
        self.DrawText(f"A: {str(self.A)}", self.pos[0], self.pos[1])
        self.DrawText(f"B: {str(self.B)}", self.pos[0], self.pos[1] + self.font_size + self.line_spacing)
        self.DrawText(f"C: {str(self.C)}", self.pos[0], self.pos[1] + self.font_size * 2 + self.line_spacing * 2)
        self.DrawText(f"D: {str(self.D)}", self.pos[0], self.pos[1] + self.font_size * 3 + self.line_spacing * 3)
        self.DrawText(f"E: {str(self.E)}", self.pos[0], self.pos[1] + self.font_size * 4 + self.line_spacing * 4)

    def DrawText(self, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.surface.blit(text_surface, text_rect)