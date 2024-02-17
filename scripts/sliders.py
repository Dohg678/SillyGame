import pygame

class Slider():
    
    def __init__(self, game, slidermax=100, slidermin=0, pos=[0, 0], height=5, uncolour=(0, 0, 0), topcolour=(0, 50, 0), specialtype=''):
        self.slider_value = 0
        self.slider_max = slidermax
        self.slider_min = slidermin
        self.uncolour = uncolour
        self.topcolour = topcolour
        self.pos = pos
        self.height = height
        self.is_on_mouse = False
        self.game = game
        self.curr_mouse_pos = [0, 0]
        self.hasgrab = False
    
    def has_grab(self, mouse_pos):
        self.curr_mouse_pos = mouse_pos
        if self.pos[1] <= self.curr_mouse_pos[1] <= self.height + self.pos[1] and self.pos[0] <= self.curr_mouse_pos[0] <= self.slider_max + self.pos[0]:
            self.hasgrab = True
        else: 
            self.hasgrab = False
    
    def update(self, mouse_pos):
        self.handle_collisions(mouse_pos)
        if self.is_on_mouse:
            self.slider_value = pygame.math.clamp(int(self.curr_mouse_pos[0] - self.pos[0]), self.slider_min, self.slider_max)
            self.game.volume = self.slider_value
    
    def render(self, surf, font):
        pygame.draw.rect(surf, (self.uncolour), (self.pos[0], self.pos[1], self.slider_max, self.height))
        pygame.draw.rect(surf, (self.topcolour), (self.pos[0], self.pos[1], self.slider_value, self.height))
        font.render(surf, str(self.slider_value), [self.pos[0] + self.slider_max + 4, self.pos[1]], scale=[1, 1], colour=(255, 255, 255, 0))
    
    def handle_collisions(self, mouse_pos):
        if self.hasgrab == True:
            self.curr_mouse_pos = mouse_pos
            if self.pos[0] <= self.curr_mouse_pos[0] <= self.slider_max + self.pos[0]:
                self.is_on_mouse = True
            else: 
                self.is_on_mouse = False
        