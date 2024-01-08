import pygame as pg

SPEED_FACTOR = 1

class ScreenSettings:
    WIDTH, HEIGHT = 800, 600
    FPS = 30*SPEED_FACTOR
    CAPTION = 'BirdGame'
    COLOR = pg.Color('darkslategray')

class BirdSettings:
    WIDTH, HEIGHT = 40, 40
    COLOR = pg.Color('brown4')
    JUMP_HEIGHT = int(HEIGHT)*SPEED_FACTOR
    GRAVITY = 4*SPEED_FACTOR

class PipeSettings:
    WIDTH, HEIGHT = 50, 160
    COLOR = pg.Color('chartreuse')
    HEIGHT_VARIANCE = ScreenSettings.HEIGHT//4
    LEFT_VARIANCE = WIDTH*2
    TOP_BOTTOM_GAP = int(BirdSettings.HEIGHT*3)
    LEFT_RIGHT_GAP = WIDTH*4
    TOP = 0
    LEFT = int(ScreenSettings.WIDTH)
    SPEED = 2*SPEED_FACTOR

class GroundSettings:
    COLOR = pg.Color('burlywood4')
    HEIGHT = ScreenSettings.HEIGHT//10
    WIDTH = ScreenSettings.WIDTH
    TOP = ScreenSettings.HEIGHT - HEIGHT 
    LEFT = 0