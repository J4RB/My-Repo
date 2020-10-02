import pygame as pg
import math
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.Surface((100, 100))
        #self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.load_images()
        self.image.blit(player_sprite, (0, 0))
        self.rect = self.image.get_rect()

        self.pos = vec(SCREEN_WIDTH /2, SCREEN_HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rotation = 0

    def load_images(self):
        player_sprite = pg.image.load('./images/spaceship.png')