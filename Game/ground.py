import pygame as pg 
from settings import GroundSettings

class Ground(pg.Rect):
    def __init__(self):
        self.color = GroundSettings.COLOR 
        self.top = GroundSettings.TOP 
        self.left = GroundSettings.LEFT
        self.height = GroundSettings.HEIGHT 
        self.width = GroundSettings.WIDTH

    def draw(self, surface) -> None:
        pg.draw.rect(surface, self.color, self)