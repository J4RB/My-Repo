import pygame as pg
from settings import *
from player import *

class Game:
    def __init__(self):
        pg.init()

        # Game window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        #pg.display.set_icon(pg.image.load('./images/icon.png'))
        
        # Game starting stage
        self.clock = pg.time.Clock()
        self.running = True

        self.load_data()


    def load_data(self):
        self.font_name = pg.font.match_font(FONT_NAME)

        # load images

    
    def new(self):
        self.run()


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        pass


    def events(self):
    # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                        


    def draw(self):
        # Game Loop - draw
        # *after* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)

        pg.display.flip()
        self.wait_for_key()

    
    def show_go_screen(self):
        # game over/continue
        if not self.running: # quit means quit and not go-screen
            return  # means end this funktion

        # draw
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 10)

        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
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
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()