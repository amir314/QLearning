import random

import pygame as pg

from settings import ScreenSettings, PipeSettings, BirdSettings

from bird import Bird
from pipe import Pipe
from ground import Ground

class ScreenRender:
    def __init__(self):
        pg.init()

        self.RES = ScreenSettings.WIDTH, ScreenSettings.HEIGHT
        self.CAPTION = ScreenSettings.CAPTION
        self.COLOR = ScreenSettings.COLOR

        self.FPS = ScreenSettings.FPS

        self.screen = pg.display.set_mode(self.RES)

        self.clock = pg.time.Clock()

        self.score = 0

        self.mode = 0

        self.immortal = 0

        self.create_objects()

    def create_objects(self) -> None:
        self.bird = Bird()

        first_top_pipe = Pipe()
        first_bottom_pipe = first_top_pipe.from_bottom()
        self.pipes = [first_top_pipe, first_bottom_pipe]

        self.ground = Ground()

    def update_pipes(self) -> None:
        last_pipe = self.pipes[-1]
        if last_pipe.is_on_screen():
            new_top_pipe = Pipe()
            new_top_pipe.left = last_pipe.right + PipeSettings.LEFT_RIGHT_GAP + random.randint(
                0,
                PipeSettings.LEFT_RIGHT_GAP
            )
            new_bottom_pipe = new_top_pipe.from_bottom()
            self.pipes += [new_top_pipe, new_bottom_pipe]

    def draw(self) -> None:
        self.screen.fill(self.COLOR)

        self.bird.draw(self.screen)

        for pipe in self.pipes:
            if pipe.is_on_screen():
                pipe.draw(self.screen)
            elif not pipe.is_alive():
                self.pipes.remove(pipe)

        self.ground.draw(self.screen)

    def move_pipes(self) -> None:
        for pipe in self.pipes:
            pipe.left -= PipeSettings.SPEED

    def apply_gravity(self) -> None:
        self.bird.top += BirdSettings.GRAVITY

    def process_event(self, event) -> None:
        if event.type == pg.QUIT:
                exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.bird.top -= self.bird.jump_height
            elif event.key == pg.K_p:
                self.mode = 1 - self.mode
            elif event.key == pg.K_i:
                self.immortal = 1 - self.immortal    

    def wait_for_event(self) -> None:
        event = pg.event.wait()
        self.process_event(event)
            
    def check_events(self) -> None:
        for event in pg.event.get():
            self.process_event(event)

    def event_handler(self) -> None:
        if self.mode == 1:
            self.wait_for_event()
        else:
            self.check_events()

    def check_collisions(self) -> None:
        if not self.bird.collidelist(self.pipes + [self.ground]) == -1 and not self.immortal:  
            self.bird.alive = False

    def check_clearence(self) -> None:
        for pipe in self.pipes:
            if pipe.right < self.bird.left and pipe.is_upside_down() and pipe.cleared == False:
                self.score += 1
                pipe.cleared = True
                print(self.score) 

    def reset(self) -> None:
        self.create_objects()
        self.score = 0

    def run(self) -> None:
        pg.event.clear()
        while True:
            self.draw()
            pg.display.set_caption(self.CAPTION)
            pg.display.flip()
            self.clock.tick(self.FPS)

            self.event_handler()
        
            self.move_pipes()
            self.update_pipes()

            self.apply_gravity()

            self.check_collisions()

            if not self.bird.is_alive():
                event = pg.event.wait()
                if event.type == pg.KEYDOWN:
                    self.reset()

            self.check_clearence()
            
            
if __name__=="__main__":
    screen = ScreenRender() 
    screen.run()