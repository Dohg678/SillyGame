#for the main settings
import pygame
from scripts.buttons import Button
from scripts.sliders import Slider

"""Classes needed:
-The main settings menu
-Key bindings and key rebinding
-Sound settings
-Video settings
"""
class Settings:
    def __init__(self, game):
        self.game = game
        self.current_menu = "main"
        self.mouseinput = [0, 0]
        self.mousedown = False
        self.fonts = self.game.fonts
        
        self.sliders = {
            'sfx': Slider(self, pos=[50, 50]),
            'music': Slider(self),
        }
        
        self.buttons = {
            'tosounds': Button(self, 'Sounds', 'soundsliders', self.fonts['small'], scale=[3, 3], pos=[24, 48]),
            'tokeybinds': Button(self, 'keybinds', 'keybinds', self.fonts['small'], scale=[3, 3], pos=[24,16]),
            'tores_opts': Button(self, 'resolution_options', 'screensize', self.fonts['small'], scale=[3, 3], pos=[24,80])
        }
        
        self.resolution_options = {
            'tiny': Button(self, '320 x 180', (320, 180), self.fonts['small'], scale=[1, 1], pos=[24, 16]),
            'small': Button(self, '480 x 270', (480, 270), self.fonts['small'], scale=[1, 1], pos=[24, 32]),
            'smallish': Button(self, '640 x 360', (640, 360), self.fonts['small'], scale=[1, 1], pos=[24, 48]),
            'normal': Button(self, '960 x 540', (960, 540), self.fonts['small'], scale=[1, 1], pos=[24, 64]),
            'large': Button(self, '1280 x 720', (1280, 720), self.fonts['small'], scale=[1, 1], pos=[24, 80]),
            'xl': Button(self, '1600 x 900', (1600, 900), self.fonts['small'], scale=[1, 1], pos=[24, 96]),
            'no': Button(self, 'no (16 x 9)', (16, 9), self.fonts['small'], scale=[1, 1], pos=[24, 112]),
        }
        
        self.return_heirarchy = {
            'mainpage': 'mainpage',
            'keybinds': 'mainpage',
            'soundsliders': 'mainpage',
            'changekey': 'keybinds',
            'screensize': 'mainpage',
        }
        

    def main(self, display):
        
        display.blit(self.game.assets['return'], (4, 4))
        if self.game.isfullscreen == 0:
            display.blit(self.game.assets['into_fullscreen'], (display.get_width() - 20, 4))
        else:
            display.blit(self.game.assets['exit_fullscreen'], (display.get_width() - 20, 4))
        
        self.buttons['tokeybinds'].render(display, self.fonts['small'])
        self.buttons['tosounds'].render(display, self.fonts['small'])
        self.buttons['tores_opts'].render(display, self.fonts['small'])
    
    def main_update(self):
        if self.mousedown:
            collisions = self.game.mpos_r.colliderect(self.game.keybinding_rect)
            if collisions:
                self.game.settings = 'keybinds'
            collisions = self.game.mpos_r.colliderect(self.game.isfullscreen_rect)
            if collisions:
                self.game.isfullscreen = not self.game.isfullscreen
                if self.game.isfullscreen:
                    self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                else:
                    self.screen = pygame.display.set_mode(self.base_screen_size, pygame.RESIZABLE)
        
            for button in self.buttons:
                action = self.buttons[button].update(self.game.mpos_r)
                if action:
                    self.game.settings = self.buttons[button].action
            collisions = self.game.mpos_r.colliderect(self.game.return_rect)
            if collisions:
                self.game.menu = 'main'
                self.game.iterations = 0
                
    def keybinds(self):
        pass
    
    def keybinds_update(self):
        pass
    
    def sounds(self, display):
        self.sliders['sfx'].render(display, self.fonts['small'])
    
    def sounds_update(self):
        if not self.mousedown:
            for slider in self.sliders:
                self.sliders[slider].hasgrab = False
        else:
            for slider in self.sliders:
                self.sliders[slider].has_grab(self.game.mpos)
                self.sliders[slider].update(self.game.mpos)
            
    
    def video(self):
        pass
    
    def video_update(self):
        pass
    
    def update(self):
        """
        input is the inputs given to the display:
        mouse = list composed of up or down, location x, location y
        keypresses = dict composed of key that is pressed, and if it is pressed or unpressed.
        """
        #contains the logic for choosing which menu to display.
        #gets inputs, location and keys pressed and passes it to the function