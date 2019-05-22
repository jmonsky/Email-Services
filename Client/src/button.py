import pygame

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
    surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

class Button(object):
    def __init__(self, name, icon = None, height=50, textSize=15, function= None):
        self.name = name
        self.textSize = textSize
        self.buttonHeight = height
        self.hover = False
        self.clicked = False
        self.length = len(self.name) * (self.textSize / 2)+ 10
        self.function = function
        self.color = (120, 120, 120)
        self.select = False
    def Click(self, *args):
        self.clicked = True
    def Selected(self):
        self.select = True
    def NoSelect(self):
        self.select = False
    def Hover(self):
        self.hover = True
    def NoHover(self):
        self.hover = False
    def CreateSurf(self):
        surf = pygame.Surface((self.length, self.buttonHeight))
        surf.fill(self.color)
        if self.hover:
            surf.fill((120, 120, 250))
        if self.select:
            surf.fill((120, 250, 120))
        if self.clicked:
            surf.fill((250, 120, 120))
        blitText(surf, self.name, (5, self.buttonHeight / 2 - self.textSize / 2))
        return surf

    def execute(self):
        if self.function != None:
            self.function()
        self.clicked = False
    