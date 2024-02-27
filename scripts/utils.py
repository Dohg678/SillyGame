import os
import json
import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if img_name != '.DS_Store':
            images.append(load_image(path + '/' + img_name))
    return images

def clip(surf, x, y, clipsizex, clipsizey):
    clip_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, clipsizex, clipsizey)
    clip_surf.set_clip(clip_rect)
    img = surf.subsurface(clip_surf.get_clip())
    return img.copy()

def fontcolour(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_bgcopy = pygame.Surface(surf.get_size())
    
    img_bgcopy.fill((0, 0, 0))
    img_bgcopy.blit(surf, (0, 0))
    img_copy.fill(new_c)
    img_bgcopy.set_colorkey(old_c)
    img_copy.blit(img_bgcopy, (0, 0))
    img_copy.set_colorkey((0, 0, 0))
    
    return img_copy
# all the characters
class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','*','"','<','>',';']
        font_img = load_image('fonts/' + path)
        current_charwidth = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_charwidth, 0, current_charwidth, font_img.get_height())
                try:
                    self.characters[self.character_order[character_count]] = char_img.copy()
                except:
                    pass
                character_count += 1
                current_charwidth = 0
            else:
                current_charwidth += 1
        self.space_width = self.characters['A'].get_width()
    
    def get_text_size(self, text='', scale=[1, 1]):
        y_offset = self.characters['A'].get_height()
        x_offset = 0
        for char in text:
            if char != ' ':
                x_offset += (self.characters[char].get_width() + self.spacing) * scale[0]
            else:
                x_offset += (self.space_width + self.spacing) * scale[0]
        return [x_offset, y_offset]
        
    def render(self, surf, text, loc, scale=[0, 0], colour=(255, 0, 0, 0), outline=True):
        y_offset = self.characters['A'].get_height()
        x_offset = 0
        for char in text:
            if char != ' ':
                try:
                    x_offset += (self.characters[char].get_width() + self.spacing) * scale[0]
                except:
                    x_offset += (self.space_width + self.spacing) * scale[0]
            else:
                x_offset += (self.space_width + self.spacing) * scale[0]
            
        tempsurf = pygame.Surface((x_offset + 10, y_offset * scale[1]))
        x_offset = 0
        for char in text:
            if char != ' ':
                try:
                    img = self.characters[char]
                except:
                    continue
                img = fontcolour(img,(255, 0, 0), colour)
                tempsurf.blit(pygame.transform.scale(img, (img.get_width() * scale[0], img.get_height() * scale[1])), (x_offset, 0))
                x_offset += (img.get_width() + self.spacing) * scale[0]
            else:
                x_offset += (self.space_width + self.spacing) * scale[0]
        tempsurf.set_colorkey((0, 0, 0))
        if outline:
            display_mask = pygame.mask.from_surface(tempsurf)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                surf.blit(display_sillhouette, (offset[0] + loc[0], offset[1] + loc[1]))
        surf.blit(tempsurf, loc)
        rect = pygame.Rect(loc[0], loc[1], x_offset, y_offset * scale[1])
        #pygame.draw.rect(surf, (10, 10, 10), rect, 1)
        return rect
        
#['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '*', '"', '<', '>', ';']

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    
 
class FileManager(): 
    
    def __init__(self, game):
        self.game = game
        
    def savefile(self, saveorload):
        load = saveorload
        if load ==  "save":
            f = open("save.SAVEFILE", 'w')
            json.dump({'level': self.game.level, 'checkpoint': self.game.respawnpoint}, f)
            f.close()
            print('sucess')
        elif load == "dump":
            try:
                f = open("save.SAVEFILE", 'r')
                savedata = json.load(f)
                f.close()
            except:
                return {'level': 0, 'checkpoint': [0, 0]}
            return savedata
        elif load == "clear":
            f = open("save.SAVEFILE", 'w')
            json.dump({}, f)
            f.close()
        else:
            print("The file does not exist")
    


    def settings(self, saveorload):
        load = saveorload
        if load ==  "save":
            f = open("settings.SAVEFILE", 'w')
            json.dump({'keybinds': self.game.keybinds, 'keybindingvalue': self.game.keybindingvalue, 'window_size': self.game.window_size}, f)
            f.close()
            
        elif load == "dump":
            f = open("settings.SAVEFILE", 'r')
            settings = json.load(f)
            f.close()
            return settings