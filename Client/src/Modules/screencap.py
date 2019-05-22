import pygame
class ScreenCap(object):
    def __init__(self, filename):
        self.orgpicture = pygame.image.load(filename.strip("'"))
        self.picture = None
        self.filename = filename
        self.Position = (0, 0)
    def update(self):
        return ScreenCap(self.filename)
    def getPicture(self):
        return self.picture
    def scale(self, x, y):
        self.picture = pygame.transform.scale(self.orgpicture, (x, y))
    def delete(self):
        pass
    def exists(self, fname):
        return fname == self.filename
