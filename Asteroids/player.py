import pygame as pg
import math

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_settings()
        self.load_images()
        self.image = pg.Surface((self.PLAYER_IMG_WIDTH, self.PLAYER_IMG_HEIGHT))
        self.image = self.player_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        self.org_image = self.image
        self.current_image = self.image

        self.pos = vec(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rotation = 90
        self.thrusting = False
        self.current_frame = 0
        

    def load_settings(self):
       # game options/settings
        self.SCREEN_WIDTH = 1802
        self.SCREEN_HEIGHT = 980

       # player properties
        self.PLAYER_IMG_WIDTH = 29
        self.PLAYER_IMG_HEIGHT = 32
        self.PLAYER_ACC = 0.01
        self.PLAYER_FRICTION = -0.009
        self.PLAYER_TURN_RATE = 0.8
        self.PLAYER_THRUST_MULTIPIER = 0.05


    def load_images(self):
        self.player_sprite = pg.image.load('./images/spaceship.png')
        self.player_sprite_thrust = pg.image.load('./images/spaceship_thrust.png')


    def state(self):
        if self.thrusting:
            self.current_image = self.player_sprite_thrust
        else:
            self.current_image = self.player_sprite


    # def animate(self):
    #     now = pg.time.get_ticks()
    #     keys = pg.key.get_pressed()
    #     if self.thrusting:
    #         self.current_frame = (self.current_frame + 1) % len(self.player_sprite_thrust)
    #         self.image = self.player_sprite_thrust[self.current_frame]


    def rotate(self, image, rect, angle): # Rotate the image while keeping its center.
        # Rotate the original image without modifying it.
        new_image = pg.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center = rect.center)
        return new_image, rect


    def ship_rotation(self):
        keys = pg.key.get_pressed()
        # Player keys for rotation
        if keys[pg.K_LEFT]:
            self.rotation += self.PLAYER_TURN_RATE
        if keys[pg.K_RIGHT]:
            self.rotation -= self.PLAYER_TURN_RATE

        # Make sure player rotation angel is not larger than 360 and smaller than 0
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
        
        self.state()
        # Run the funktion 'rotate' in order to rotate the player
        self.image, self.rect = self.rotate(self.current_image, self.rect, self.rotation - 90)


    def thrust(self):
        # Move player in direction faceing
        # Convert degrees to radians
        self.rotation = (self.rotation * math.pi) / 180
        # Determine the direction the player is faceing and accelerate
        thrust = vec(math.cos(self.rotation), -math.sin(self.rotation))
        # Thrust when key up pressed
        self.vel += thrust * self.PLAYER_THRUST_MULTIPIER
        # Convert radians back to degrees
        self.rotation = (self.rotation * 180) / math.pi

    def boarderCollisionCheck(self):
        # wrap around the sides of the screen
        if self.pos.x > self.SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.SCREEN_WIDTH
        if self.pos.y > self.SCREEN_HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = self.SCREEN_HEIGHT

    def update(self):
        #self.animate()
        self.acc = vec(0, 0)
        # apply friction
        self.acc += self.vel * self.PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.boarderCollisionCheck()
        self.state()
        self.ship_rotation()
        self.rect.center = self.pos