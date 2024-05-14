import sys
import os
import pygame
import cProfile

from scripts.utils import load_images, Font
from scripts.tilemap import Tilemap

clickeffectsize = 50
RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()
        

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
        self.display = pygame.Surface((480, 270))
        self.display_scaled = pygame.Surface((960, 540))
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'base': load_images('tiles/base_demo_tiles'),
            'bouncepad': load_images('tiles/bounce_pad'),
            'tutorial': load_images('tiles/tut'),
            'cameratr': load_images('tiles/triggers/camera'),
            'kill': load_images('tiles/kill'),
            'killbricks': load_images('tiles/killbricks'),
            'ice': load_images('tiles/ice'),
            'decor': load_images('tiles/decor'),
            'breakables': load_images('tiles/Breakables'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners'),
            'checkpoint': load_images('tiles/checkpoint'),
        }
        
        self.smallfont = Font('small_font.png')
        
        self.movement = [False, False, False, False]
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.level = 0
        try:
            self.tilemap.load('data/maps/' + str(self.level) + '.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.scroll_amt = 2
        self.current_layer = 0
        self.startclickpoint = []
        self.endclickpoint = []
        self.clickmode = 'pen'
        self.clickmodes = ['pen', 'rect', 'rubber']
        self.layers = ['rooms', 'fgscaled', 'fg', 'triggers', 'invis']
    
    def remove_tile(self, tile_pos, mpos):
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap.tilemap[self.layers[self.current_layer]]:
            del self.tilemap.tilemap[self.layers[self.current_layer]][tile_loc]
        for tile in self.tilemap.offgrid_tiles.copy():
            tile_img = self.assets[tile['type']][tile['variant']]
            tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
            if tile_r.collidepoint(mpos):
                self.tilemap.offgrid_tiles.remove(tile)
    
    def make_rect(self): 
        #makes rect, checks for the direction of drag and the creates an x and y for loop that adds the tiles to the tilemap.
        
        if self.endclickpoint[0] <= self.startclickpoint[0]:
            for x in range(self.startclickpoint[0] - self.endclickpoint[0] + 1):
                if self.endclickpoint[1] <= self.startclickpoint[1]:
                    for y in range(self.startclickpoint[1] - self.endclickpoint[1] + 1):
                        #+ 1 and - 1 are to offset the positions so that it renders correctly.
                        self.tilemap.tilemap[self.layers[self.current_layer]][str(self.endclickpoint[0] + x) + ';' + str(self.endclickpoint[1] + y)] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': [self.endclickpoint[0] + x, self.endclickpoint[1] + y]}
                else:
                    for y in range(self.endclickpoint[1] - self.startclickpoint[1] + 1):
                        self.tilemap.tilemap[self.layers[self.current_layer]][str(self.endclickpoint[0] + x) + ';' + str(self.startclickpoint[1] + y)] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': [self.endclickpoint[0] + x, self.startclickpoint[1] + y]}
                
        else:
            for x in range(self.endclickpoint[0] - self.startclickpoint[0] + 1):
                if self.endclickpoint[1] <= self.startclickpoint[1]:
                    for y in range(self.startclickpoint[1] - self.endclickpoint[1] + 1):
                        self.tilemap.tilemap[self.layers[self.current_layer]][str(self.startclickpoint[0] + x) + ';' + str(self.endclickpoint[1] + y)] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': [self.startclickpoint[0] + x, self.endclickpoint[1] + y]}
                else:
                    for y in range(self.endclickpoint[1] - self.startclickpoint[1] + 1):
                        self.tilemap.tilemap[self.layers[self.current_layer]][str(self.startclickpoint[0] + x) + ';' + str(self.startclickpoint[1] + y)] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': [self.startclickpoint[0] + x, self.startclickpoint[1] + y]}
    
    def make_tile(self, tile_pos):
        self.tilemap.tilemap[self.layers[self.current_layer]][str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_amt
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_amt
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            iterationlayer = 0
            for layer in self.tilemap.tilemap:
                
                if layer != self.current_layer:
                    self.tilemap.editorrender(self.display, self.layers[iterationlayer], opacity=100, offset=render_scroll)
                iterationlayer += 1
            self.tilemap.editorrender(self.display, self.layers[self.current_layer], offset=render_scroll)
                
            self.tilemap.show_cam_bounds(self.display, self.layers[self.current_layer], offset=render_scroll)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tileset = self.tile_list[self.tile_group]
            current_tile_img.set_alpha(100)
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
                self.tilemap.autotile()
            else:
                self.display.blit(current_tile_img, mpos)
            
            if self.clicking and self.ongrid and self.clickmode == 'pen':
                self.make_tile(tile_pos)
                
            if self.right_clicking:
                self.remove_tile(tile_pos, mpos)
                        
            if self.clicking:
                pygame.draw.rect(self.display, (255, 200, 50), (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1], 16, 16))
            else:
                pygame.draw.rect(self.display, (255, 200, 50), (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1], 16, 16), 1)
           
                
            self.display.blit(current_tile_img, (5, 5))
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                        if self.clickmode == 'rect':
                            self.startclickpoint = list(tile_pos)
                            
                        
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                        if self.clickmode == 'rect':
                            self.endclickpoint = list(tile_pos)
                            self.make_rect()
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.right_clicking = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_9:
                        self.current_layer = max(self.current_layer - 1, 0)
                    if event.key == pygame.K_0:
                        self.current_layer = min(self.current_layer + 1, len(self.layers) - 1)
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_r:
                        self.clickmode = 'rect'
                    if event.key == pygame.K_p:
                        self.clickmode = 'pen'
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('data/maps/' + str(self.level) + '.json')
                    if event.key == pygame.K_n:
                        self.tilemap.save('data/maps/' + str(self.level) + '.json')
                        self.level += 1 
                        try:
                            self.tilemap.load('data/maps/' + str(self.level) + '.json')
                        except FileNotFoundError:
                            pass
                    if event.key  == pygame.K_SPACE:
                        self.right_clicking = True
                    if self.shift:
                        if event.key == pygame.K_4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.key == pygame.K_5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.key == pygame.K_4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.key == pygame.K_5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_EQUALS:
                        self.scroll_amt = min(self.scroll_amt * 2, 16)
                    if event.key == pygame.K_MINUS:
                        self.scroll_amt = max(self.scroll_amt / 2, 0.5)
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            
            self.tilemap.rendertilehb(self.display, self.layers[self.current_layer], render_scroll)
            try:
                self.hover_tile = str(self.tilemap.tilemap[self.layers[self.current_layer]][str(tile_pos[0]) + ';' + str(tile_pos[1])])
            except:
                self.hover_tile = 'none'
            self.smallfont.render(self.display, current_tileset, (25, 5), (1, 1))
            self.smallfont.render(self.display, str(self.clock.get_fps()), (25, 28), (1, 1))
            self.smallfont.render(self.display, self.hover_tile, (25, 21), (1, 1))
            self.smallfont.render(self.display, self.layers[self.current_layer], (25, 13), (1, 1))
            self.smallfont.render(self.display, self.clickmode, (25, 35), (1, 1))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()
#cProfile.run('Editor().run()')