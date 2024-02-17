import pygame



class Button():
    
    def __init__(self, game, text, action, font, size=[1, 1], pos=[0, 0], fontcolour=(255, 255, 255), specialtype=''):
        self.slider_value = 0
        self.fontcolour = fontcolour
        self.text = text
        self.size = font.get_text_size(self.text, [1, 1])
        self.pos = pos
        self.is_on_mouse = False
        self.game = game
        self.action = action
        self.curr_mouse_pos = [0, 0]
    
    
    def update(self, mouse_pos):
        self.handle_collisions(mouse_pos)
        if self.is_on_mouse:
            return True
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def render(self, surf, font, scale=[1, 1]):
        self.size = font.get_text_size(self.text, [1, 1])
        font.render(surf, self.text, self.pos, scale=scale, colour=(255, 255, 255, 0))
    
    def handle_collisions(self, mouse_pos):
        self.curr_mouse_pos = mouse_pos
        if self.pos[0] <= self.curr_mouse_pos[0] <= self.size[0] + self.pos[0] and self.pos[1] <= self.curr_mouse_pos[1] <= self.size[1] + self.pos[1]:
            self.is_on_mouse = True
        else: 
            self.is_on_mouse = False
        