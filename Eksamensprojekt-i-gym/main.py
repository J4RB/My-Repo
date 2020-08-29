# Ninja Wall Jump! - platformer
import pygame as pg
import random
from settings import *
from sprites import *
from database import Highscore_data
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.mixer.music.set_volume(MUSIC_VOLUME)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load('./images/icon.png'))
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        # database
        self.data = Highscore_data()
        self.data.create_tables()

        self.load_data()

    def load_data(self):
        # load highscores
        highscores = self.data.get_highscore_list()
        self.best_10_highscores = self.data.N_max_elements(highscores, 10)

        # load images
        self.background = pg.image.load('./images/Forrest_Background_1.png')
        self.midground = pg.image.load('./images/Forrest_Midground_1.png')
        self.player_sprite_menu = pg.image.load('./images/standing.png')
        self.player_sprite_menu = pg.transform.scale(self.player_sprite_menu, (PLAYER_IMG_WIDTH * 12, PLAYER_IMG_HEIGHT * 12))

        # load sounds
        self.dir = path.dirname(__file__)
        self.sounds_dir = path.join(self.dir, 'sounds')
        self.jump_sound = pg.mixer.Sound(path.join(self.sounds_dir, 'jump.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.sounds_dir, 'boost.wav'))
    
    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.left_wall_platforms = pg.sprite.Group()
        self.right_wall_platforms = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat) # (*plat) - Takes all of the arguments for the platform, called explode a list
        for left_wall_plat in LEFT_WALL_PLATFORM_LIST:
            p = Platform_Wall(self, *left_wall_plat)
            self.all_sprites.add(p)
            self.left_wall_platforms.add(p)
        for right_wall_plat in RIGHT_WALL_PLATFORM_LIST:
            p = Platform_Wall(self, *right_wall_plat)
            self.all_sprites.add(p)
            self.right_wall_platforms.add(p)
        self.mob_timer = 0
        self.run()

    def run(self):
        # load and play game music
        pg.mixer.music.load('./sounds/game_the_end.ogg')
        pg.mixer.music.play(-1, 0)

        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
        # fadeout music
        pg.mixer.music.fadeout(500)     # 500ms

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):    # How often should a mob spawn?
            self.mob_timer = now
            Mob(self)
        # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]        # Make sure that the player snaps to the lowest platform, prevents snaping up if the player walk over a higher platform
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        hits_left = pg.sprite.spritecollide(self.player, self.left_wall_platforms, False)
        if hits_left:
            self.player.pos.x = hits_left[0].rect.right
            self.player.vel.y = 0

        hits_right = pg.sprite.spritecollide(self.player, self.right_wall_platforms, False)
        if hits_right:
            self.player.pos.x = hits_right[0].rect.left
            self.player.vel.y = 0
        
        # if player reaches top 1/4 of screen, scroll
        if self.player.rect.top <= HEIGHT / 4:                      # scroll platforms
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)

            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            
            for plat in self.left_wall_platforms:                   # scroll left wall
                plat.rect.y += 5
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            
            for plat in self.right_wall_platforms:                  # scroll right wall
                plat.rect.y += 5
                if plat.rect.top >= HEIGHT:
                    plat.kill()
        
        # if player hits a powerup
        powerup_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            #self.load_data()
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 4:
            max_plat_width = 96
            Platform(self, random.randrange(65, WIDTH - max_plat_width - 55),
                           random.randrange(-75, -30))

        while len(self.left_wall_platforms) < 2:
            p = Platform_Wall(self, 0, -HEIGHT)
            self.left_wall_platforms.add(p)
            self.all_sprites.add(p)

        while len(self.right_wall_platforms) < 2:
            p = Platform_Wall(self, WIDTH - 42, -HEIGHT)
            self.right_wall_platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.midground, (0,0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        # load and play intro music
        pg.mixer.music.load('./sounds/intro_green_forest.ogg')
        pg.mixer.music.play(-1, 0)

        # draw
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.player_sprite_menu, (WIDTH / 2 - PLAYER_IMG_WIDTH * 12 / 2 + 10, HEIGHT / 2 - PLAYER_IMG_HEIGHT * 12 / 2 + 30))
        self.draw_text(TITLE, 56, WHITE, WIDTH / 2, HEIGHT / 7)
        self.draw_text("Arrows to move, Space to jump", 20, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3.2 / 4)
        if len(self.best_10_highscores) > 0:
            self.draw_text("High Score: " + str(self.best_10_highscores[0][1]), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        pg.display.flip()
        self.wait_for_key()

        #fadeout music
        pg.mixer.music.fadeout(500)     # 500ms

    def show_go_screen(self):
        # game over/continue
        # load and play intro music
        pg.mixer.music.load('./sounds/intro_green_forest.ogg')
        pg.mixer.music.play(-1, 0)

        if not self.running: # quit means quit and not go-screen
            return  # means end this funktion

        # draw
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 10)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 4 - 10)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3.2 / 4)
        
        if self.score > self.best_10_highscores[9][1]:
            self.data.db.execute("""INSERT INTO highscores (score) VALUES (?);""", (self.score,))
            # update the database with the new changes
            self.data.db.commit()
            # load highscores
            highscores = self.data.get_highscore_list()
            self.best_10_highscores = self.data.N_max_elements(highscores, 10)
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 24)
            for index, highscore in enumerate(self.best_10_highscores):     # enumerate adds a counter (index) 
                self.draw_text(str(highscore[1]), 18, WHITE, WIDTH / 2 + 90, HEIGHT / 3 + 22 * index)
                self.draw_text(str(highscore[0]), 18, WHITE, WIDTH / 2 - 10, HEIGHT / 3 + 22 * index)
                self.draw_text(str("{}.").format(index + 1), 18, WHITE, WIDTH / 2 - 100, HEIGHT / 3 + 22 * index)
        else:
            for index, highscore in enumerate(self.best_10_highscores):
                self.draw_text(str(highscore[1]), 18, WHITE, WIDTH / 2 + 90, HEIGHT / 3 + 22 * index)
                self.draw_text(str(highscore[0]), 18, WHITE, WIDTH / 2 - 10, HEIGHT / 3 + 22 * index)
                self.draw_text(str("{}.").format(index + 1), 18, WHITE, WIDTH / 2 - 100, HEIGHT / 3 + 22 * index)
        pg.display.flip()
        self.wait_for_key()

        #fadeout music
        pg.mixer.music.fadeout(500)     # 500ms

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
