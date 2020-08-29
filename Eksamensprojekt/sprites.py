# sprite classes for platform game
import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT - 40)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames_temp = [pg.image.load('./images/standing.png'),
                                     pg.image.load('./images/standing_1.png')]      # Add a flipped idle animation
        self.standing_frames = []
        for frame in self.standing_frames_temp:
            self.standing_frames.append(pg.transform.scale(frame, (PLAYER_IMG_WIDTH * PLAYER_SCALE, PLAYER_IMG_HEIGHT * PLAYER_SCALE)))
        
        self.walk_frames_r_temp = [pg.image.load('./images/run_0.png'),
                              pg.image.load('./images/run_1.png'),
                              pg.image.load('./images/run_2.png'),
                              pg.image.load('./images/run_3.png'),
                              pg.image.load('./images/run_4.png'),
                              pg.image.load('./images/run_5.png'),
                              pg.image.load('./images/run_6.png')]
        self.walk_frames_r = []
        for frame in self.walk_frames_r_temp:
            self.walk_frames_r.append(pg.transform.scale(frame, (PLAYER_IMG_WIDTH * PLAYER_SCALE, PLAYER_IMG_HEIGHT * PLAYER_SCALE)))
        
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        
        self.jump_frame_r = pg.image.load('./images/jump.png')                   # Add a flipped jump spirte
        self.jump_frame_r = pg.transform.scale(self.jump_frame_r, (PLAYER_IMG_WIDTH * PLAYER_SCALE, PLAYER_IMG_HEIGHT * PLAYER_SCALE))

        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)

        self.wall_stick_r = pg.image.load('./images/wall_stick.png')
        self.wall_stick_r = pg.transform.scale(self.wall_stick_r, (PLAYER_IMG_WIDTH * PLAYER_SCALE, PLAYER_IMG_HEIGHT * PLAYER_SCALE))

        self.wall_stick_l = pg.transform.flip(self.wall_stick_r, True, False)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:     # If moving upwards y is negative, 3 if just a number
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        # checks to see if the player is standing on a platform, if so the player can jump
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        hits_left = pg.sprite.spritecollide(self, self.game.left_wall_platforms, False)
        hits_right = pg.sprite.spritecollide(self, self.game.right_wall_platforms, False)
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
        if hits_left:
            self.game.jump_sound.play()
            self.vel.x += 30
            self.vel.y -= 20
        if hits_right:
            self.game.jump_sound.play()
            self.vel.x -= 30
            self.vel.y -= 20

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        if self.jumping and self.vel.x > 0:         # jumping right sprite
            self.image = self.jump_frame_r
        if self.jumping and self.vel.x < 0:         # jumping left sprite
            self.image = self.jump_frame_l

        hits_left = pg.sprite.spritecollide(self, self.game.left_wall_platforms, False)
        hits_right = pg.sprite.spritecollide(self, self.game.right_wall_platforms, False)
        if hits_left or hits_right:
            self.pos += self.vel + self.acc * PLAYER_WALL_FRICTION
            if hits_left:
                self.rect.midleft = self.pos
                self.image = self.wall_stick_l
            if hits_right:
                self.rect.midright = self.pos
                self.image = self.wall_stick_r
        else:
            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            # equations of motion
            self.vel += self.acc
            if abs(self.vel.x) < 0.1:       # stops walking animation eventhough player standing still
                self.vel.x = 0
            self.pos += self.vel + 0.5 * self.acc
            self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [pg.image.load('./images/log_0.png'),
                  pg.image.load('./images/log_1.png')]
        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWERUP_SPAWN_PCT:
            Powerup(self.game, self)

class Platform_Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('./images/log_wall.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POWERUP_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = pg.image.load('./images/powerup_boost.png')
        self.image = pg.transform.scale(self.image, (int(BOOST_IMG_WIDTH / 2), int(BOOST_IMG_HEIGHT / 2)))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = pg.image.load('./images/bird.png')
        self.image_up = pg.transform.scale(self.image_up, (int(MOB_IMG_WIDTH / 5), int(MOB_IMG_HEIGHT / 5)))
        self.image_down = pg.image.load('./images/bird.png')        # replace with different bird stance for animation
        self.image_down = pg.transform.scale(self.image_down, (int(MOB_IMG_WIDTH / 5), int(MOB_IMG_HEIGHT / 5)))
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()