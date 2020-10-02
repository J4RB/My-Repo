import pygame as pg
import math
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.Surface((100, 100))
        #self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        #self.image.blit(player_sprite, (0, 0))
        pg.draw.polygon(self.image, RED, [(10,10), (15,15), (20,20)])
        self.rect = self.image.get_rect()

        pg.draw.rect(self.image, RED, (10,10,10,10))

        self.pos = vec(SCREEN_WIDTH /2, SCREEN_HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rotation = 0
