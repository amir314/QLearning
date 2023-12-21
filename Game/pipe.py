import pygame as pg 

import random

from settings import ScreenSettings, PipeSettings

class Pipe(pg.Rect):
    def __init__(self):
        super().__init__(
            PipeSettings.LEFT,
            PipeSettings.TOP,
            PipeSettings.WIDTH,
            PipeSettings.HEIGHT + random.randint(
                                        -PipeSettings.HEIGHT_VARIANCE, 
                                        PipeSettings.HEIGHT_VARIANCE
                                    )
        )

        self.upside_down = True

        self.cleared = False

        self.color = PipeSettings.COLOR

    def is_on_screen(self) -> bool:
        return self.is_alive() and self.left < ScreenSettings.WIDTH
    
    def is_alive(self) -> bool:
        return self.left > 0
    
    def from_bottom(self):
        new_pipe = Pipe()

        new_pipe.left = self.left
        new_pipe.top = self.height + PipeSettings.TOP_BOTTOM_GAP
        new_pipe.height = ScreenSettings.HEIGHT - new_pipe.top

        new_pipe.upside_down = False

        return new_pipe
    
    def is_upside_down(self) -> bool:
        return self.upside_down
    
    def draw(self, surface) -> None:
        pg.draw.rect(surface, self.color, self)
