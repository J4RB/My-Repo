import pygame as pg
from player import *
from button import *
from math import floor
#from pygame import K_SPACE

class Game:
    def __init__(self):
        pg.init()

        # Game window
        self.load_settings()
        self.load_images()
        if self.FULLSCREEN_MODE:
            self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption(self.TITLE)
        pg.display.set_icon(self.icon_image)
        
        # Game starting stage
        self.clock = pg.time.Clock()
        self.running = True

    def load_settings(self):
        # game options/settings
        self.TITLE = "Asteroids"
        self.SCREEN_WIDTH = 1802
        self.SCREEN_HEIGHT = 980
        self.FPS = 120
        self.FULLSCREEN_MODE = False

        # define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (15, 15, 15)

        # define font
        self.font_name = 'Century Gothic'

    def load_images(self):
        # load images
        self.icon_image = pg.image.load('./images/spaceship.png')

    def create_buttons(self):
        # creates the buttons
        self.all_buttons = pg.sprite.Group()

        btn_font_size = floor((self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 75)
        menu_btn_font = pg.font.SysFont(self.font_name, btn_font_size)
        self.options_button = Button(
            320, 70, 170, 65, self.show_options_screen,
            menu_btn_font, 'OPTIONS', self.WHITE,
            IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)

        self.all_buttons.add(self.options_button)
    

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
        self.all_buttons.update()


    def events(self):
    # Game Loop - events
        for event in pg.event.get():
            # check for quiting game
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                # check for closing window
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

            for button in self.all_buttons:
                button.handle_event(event)
                
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
        self.screen.fill(self.BLACK)
        self.draw_text("ASTEROIDS", floor((self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 18), self.WHITE, floor(self.SCREEN_WIDTH / 2), floor(self.SCREEN_HEIGHT / 4))
        self.draw_text("PRESS SPACE TO PLAY", floor((self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 75), self.WHITE, floor(self.SCREEN_WIDTH / 2), floor(self.SCREEN_HEIGHT / 2.3))

        #self.draw_text("OPTIONS", floor((self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 75), self.WHITE, floor(self.SCREEN_WIDTH / 2), floor(self.SCREEN_HEIGHT / 1.8))
        self.create_buttons()

        pg.display.flip()
        self.wait_for_key(pg.K_SPACE)

    def show_options_screen(self):
        # options screen
        if not self.running: # quit means quit and not go-screen
            return  # means end this funktion

        self.screen.fill(self.BLACK)
        self.draw_text("OPTIONS", 48, self.WHITE, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 10)

        pg.display.flip()
        # TODO: Use different key than space, maybe escape
        self.wait_for_key(pg.K_SPACE)
    
    def show_go_screen(self):
        # game over/continue
        if not self.running: # quit means quit and not go-screen
            return  # means end this funktion

        # draw
        self.screen.fill(self.BLACK)
        self.draw_text("GAME OVER", 48, self.WHITE, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 10)

        pg.display.flip()
        self.wait_for_key(pg.K_SPACE)


    def wait_for_key(self, customKey):
        waiting = True
        keys = pg.key.get_pressed()
        while waiting:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.running = False
                    if event.key == customKey:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()

pg.quit()