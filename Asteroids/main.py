import pygame as pg
from player import *

class Game:
    def __init__(self):
        pg.init()

        # Game window
        self.load_settings()
        self.load_images()
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))#, pg.FULLSCREEN)
        pg.display.set_caption(self.TITLE)
        pg.display.set_icon(self.icon_image)
        
        # Game starting stage
        self.clock = pg.time.Clock()
        self.running = True


    def load_settings(self):
        # game options/settings
        self.TITLE = "Asteroids"
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.FPS = 60

        # define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (15, 15, 15)
        self.RED = (255, 0, 0)
        self.BGCOLOR = self.WHITE


    def load_images(self):
        # load images
        self.icon_image = pg.image.load('./images/spaceship.png')
    

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        self.run()


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # Game loop - Update
        self.all_sprites.update()


    def events(self):
    # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                # check for closing window
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.player.thrusting = True
            self.player.thrust()
        else:
            self.player.thrusting = False
        if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
            self.player.ship_rotation()


    def draw(self):
        # Game Loop - draw
        # *after* drawing everything, flip the display
        self.screen.fill((self.BLACK))
        self.all_sprites.draw(self.screen)
        
        pg.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(self.BGCOLOR)

        pg.display.flip()
        self.wait_for_key()

    
    def show_go_screen(self):
        # game over/continue
        if not self.running: # quit means quit and not go-screen
            return  # means end this funktion

        # draw
        self.screen.fill(self.BGCOLOR)
        self.draw_text("GAME OVER", 48, self.WHITE, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 10)

        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
#g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()

pg.quit()