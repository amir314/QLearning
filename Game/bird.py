import pygame as pg 

from settings import ScreenSettings, BirdSettings

class Bird(pg.Rect):
    def __init__(self):
        super().__init__(
            ScreenSettings.WIDTH//2 - BirdSettings.WIDTH//2, 
            ScreenSettings.HEIGHT//2 - BirdSettings.HEIGHT//2,
            BirdSettings.WIDTH, 
            BirdSettings.HEIGHT
        )

        self.jump_height = BirdSettings.JUMP_HEIGHT

        self.alive = True

        self.color = BirdSettings.COLOR

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self)

    def is_alive(self):
        return self.alive