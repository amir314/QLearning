import random
import math

import pygame as pg

from settings import ScreenSettings, PipeSettings, BirdSettings
from bird import Bird
from pipe import Pipe
from ground import Ground

class GameScreenRender:
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

        self.survival_time = 0

        self.create_objects()

    def create_objects(self) -> None:
        self.bird = Bird()

        first_top_pipe = Pipe()
        first_bottom_pipe = first_top_pipe.from_bottom()
        self.pipes = [first_top_pipe, first_bottom_pipe]

        self.ground = Ground()

    def add_pipes(self) -> None:
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
            if event.key == pg.K_SPACE and self.bird.top > 0:
                self.bird.top -= self.bird.jump_height
            elif event.key == pg.K_b:
                pass
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

    def action_to_event(self, action:list[int]):
        event = pg.event.Event(pg.KEYDOWN)
        if action == [1, 0]: 
            event.key = pg.K_SPACE
        elif action == [0, 1]:
            event.key = pg.K_b
        return event

    def reset(self) -> None:
        self.create_objects()
        self.score = 0

    def update_ui(self):
        self.draw()
        self.clock.tick(self.FPS)
        pg.display.flip()
        pg.display.set_caption(self.CAPTION)

    def check_alive(self):
        if not self.bird.is_alive():
            self.reset()

    def get_nearest_pipe(self):
        for i in range(len(self.pipes)):
            pipe = self.pipes[i]
            if pipe.left > self.bird.right:
                return pipe

    def get_bird_pipe_alignment(self):
        nearest_pipe = self.get_nearest_pipe()
        bird_center_y = self.bird.center[1]
        nearest_pipe_center_y = nearest_pipe.bottom + nearest_pipe.top_bottom_gap//2
        return abs(bird_center_y - nearest_pipe_center_y)

    def frame_step(self, action=None):
        if action:
            event = self.action_to_event(action)
            self.process_event(event)
        else:
            self.check_events()

        self.move_pipes()
        self.add_pipes()

        self.apply_gravity()
        self.check_collisions()
        self.check_clearence()

        self.update_ui()

        #self.survival_time += 1
        alignment = self.get_bird_pipe_alignment()

        reward = self.score*10 + 10*math.pow((ScreenSettings.HEIGHT//2-alignment)/(ScreenSettings.HEIGHT//2),3)

        return reward, 1-self.bird.is_alive(), self.score

    def get_state(self):
        alive_state = int(self.bird.is_alive())
        
        pipe = self.get_nearest_pipe()
        pipes_state_packed = [(pipe.left, pipe.bottom, pipe.width, pipe.height)]
        # Unpack pipes_status_packed
        pipes_state = []
        for pipe_state in pipes_state_packed:
            pipes_state += pipe_state
        
        bird_state = list((self.bird.left, self.bird.top, self.bird.width, self.bird.height))

        return [alive_state] + pipes_state + bird_state

    def run(self) -> None:
        while True:
            self.frame_step()
            self.check_alive()
            print(len(self.get_state()))
            
            
if __name__=="__main__":
    screen = GameScreenRender() 
    screen.run()