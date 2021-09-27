import pygame
from math import floor

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset = -100
        self.menu_text_offset = self.game.DISPLAY_H / 17
        self.heading_font_size = floor((self.game.DISPLAY_W + self.game.DISPLAY_H) / 18)
        self.heading2_font_size = floor((self.game.DISPLAY_W + self.game.DISPLAY_H) / 30)
        self.heading3_font_size = floor((self.game.DISPLAY_W + self.game.DISPLAY_H) / 50)
        self.text_font_size = floor((self.game.DISPLAY_W + self.game.DISPLAY_H) / 80)

    def draw_cursor(self):
        self.game.draw_text('*', self.heading3_font_size, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.game.DISPLAY_H / 2.3
        self.optionsx, self.optionsy = self.mid_w, self.starty + self.menu_text_offset
        self.creditsx, self.creditsy = self.mid_w, self.optionsy + self.menu_text_offset
        self.quitx, self.quity = self.mid_w, self.creditsy + self.menu_text_offset
        self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('ASTEROIDS', self.heading_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text("START", self.heading3_font_size, self.startx, self.starty)
            self.game.draw_text("OPTIONS", self.heading3_font_size, self.optionsx, self.optionsy)
            self.game.draw_text("CREDITS", self.heading3_font_size, self.creditsx, self.creditsy)
            self.game.draw_text("QUIT", self.heading3_font_size, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.cursor_offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.cursor_offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.cursor_offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.cursor_offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                self.game.running, self.game.playing = False, False
                self.game.curr_menu.run_display = False
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.game.DISPLAY_H / 2.3
        self.controlsx, self.controlsy = self.mid_w, self.voly + self.menu_text_offset
        self.cursor_rect.midtop = (self.volx + self.cursor_offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((self.game.BLACK))
            self.game.draw_text('OPTIONS', self.heading2_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text("VOLUME", self.heading3_font_size, self.volx, self.voly)
            self.game.draw_text("CONTROLS", self.heading3_font_size, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.cursor_offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.cursor_offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.textx, self.texty = self.mid_w, self.game.DISPLAY_H / 2.3

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('CREDITS', self.heading2_font_size, self.mid_w, self.game.DISPLAY_H / 4)
            self.game.draw_text('Made by me :)', self.text_font_size, self.textx, self.texty)
            self.blit_screen()
