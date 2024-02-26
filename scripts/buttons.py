import pygame



class Button():
    
    def __init__(self, game, text, action, font, scale=[1, 1], pos=[0, 0], fontcolour=(255, 255, 255), specialtype=''):
        self.slider_value = 0
        self.fontcolour = fontcolour
        self.text = text
        self.size = font.get_text_size(self.text, [1, 1])
        self.scale = scale
        self.pos = pos
        self.is_on_mouse = False
        self.game = game
        self.action = action
        self.curr_mouse_pos = [0, 0]
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0] * self.scale[0], self.size[1] * self.scale[1])
    
    def collide(self, mouse_rect):
        if self.get_rect().colliderect(mouse_rect):
            return True
        else:
            return False
    
    def update(self, mouse_rect):
        
        if self.collide(mouse_rect):
            return True
    def render(self, surf, font):
        font.render(surf, self.text, self.pos, scale=self.scale, colour=self.fontcolour)
