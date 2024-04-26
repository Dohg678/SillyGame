#!/usr/bin/env python
import os
import sys
import math
import random
import time
import pygame
import cProfile

from scripts.utils import load_image, load_images, Animation, Font, fontcolour, clip, FileManager
from scripts.entities import PhysicsEntity, Enemy, Breakable, Shard, Enemydead
from scripts.player import Player
from scripts.sliders import Slider
from scripts.buttons import Button
from scripts.musicmanager import MusicManager, SoundSource
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

#math circles

class Game:
    def __init__(self):
        self.FM = FileManager(self)
        try:
            self.settings_vals = self.FM.settings("dump")
        except:
            self.settings_vals = {'keybinds': {'left': pygame.K_LEFT,'right': pygame.K_RIGHT,'jump': pygame.K_UP,'down': pygame.K_DOWN,'dash': pygame.K_x,'menu': pygame.K_m,'respawn': pygame.K_r,'restore defaults': 'the gloop'}, 'window_size': [960, 540]}
        self.window_size = self.settings_vals['window_size']
        self.ab = 60
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100, -16, 2, 0) # setup mixer to avoid sound lag 
        pygame.init()                      #initialize pygame 
        pygame.mixer.init()
        pygame.mixer.set_num_channels(64)
        print('initiated')
        self.base_screen_size = [960, 540]
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        pygame.display.set_caption('5')
        try:
            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE, vsync=0)
        except:
            self.screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE, vsync=0)
        self.display = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 180))
        self.display_3 = pygame.Surface((320, 180))
        self.window_size = pygame.display.get_window_size()
        
        
        self.clock = pygame.time.Clock()
        self.menu = "main"
        self.movement = [False, False]
        
        self.assets = {
            'killbricks': load_images('tiles/killbricks'),
            'base': load_images('tiles/base_demo_tiles'),
            'kill': load_images('tiles/kill'),
            'bouncepad': load_images('tiles/bounce_pad'),
            'cameratr': load_images('tiles/invis/camera'),
            'ice': load_images('tiles/ice'),
            'tutorial': load_images('tiles/tut'),
            'decor': load_images('tiles/decor'),
            'checkpoint': load_images('tiles/checkpoint'),
            'breakable': load_image('entities/Breakables/idle/0.png'),
            'breakable/idle': Animation(load_images('entities/Breakables/idle'), img_dur=6),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('bg.png'),
            'grassicon': load_image('icon/grass_icon.png'),
            'transition_twirl': load_image('transitions/twirl_transition.png'),
            'menubackground': load_image('bg.png'),
            'testbutton': load_image('buttons/buttons.png'),
            'settings': load_image('buttons/settings.png'),
            'settingsbg': load_image('buttons/settings_bg.png'),
            'pausebg': load_image('buttons/settings_bg.png'),
            'pause': load_image('buttons/pause.png'),
            'return': load_image('buttons/return.png'),
            'into_fullscreen': load_image('buttons/into_fullscreen.png'),
            'exit_fullscreen': load_image('buttons/outof_fullscreen.png'),
            'clouds': load_images('clouds'),
            'overlay': load_image('overlay.png'),
            'settings_tile_scroll': load_image('buttons/tile_scroll.png'),
            'settings_tile_scroll_rev': load_image('buttons/tile_scroll_rev.png'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'checkpoint/idle': Animation(load_images('entities/checkpoint/idleoff'), img_dur=6),
            'checkpoint/idleon': Animation(load_images('entities/checkpoint/idleon'), img_dur=6),
            'checkpoint/turnon': Animation(load_images('entities/checkpoint/turnon'), img_dur=120, loop =False),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/hit': Animation(load_images('particles/hit'), img_dur=10, loop=False),
            'particle/walkdust': Animation(load_images('particles/walkdust'), img_dur=6, loop=False),
            'particle/impactdust': Animation(load_images('particles/walk'), img_dur=6, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'breakablea/idle': Animation(load_images('particles/Breakables/a/idle'), img_dur=120, loop=False),
            'breakableb/idle': Animation(load_images('particles/Breakables/b/idle'), img_dur=120, loop=False),
            'breakablec/idle': Animation(load_images('particles/Breakables/c/idle'), img_dur=120, loop=False),
            'deada/idle': Animation(load_images('particles/enemydeath/a/idle'), img_dur=15, loop=False),
            'deadb/idle': Animation(load_images('particles/enemydeath/b/idle'), img_dur=15, loop=False),
            'deadc/idle': Animation(load_images('particles/enemydeath/c/idle'), img_dur=15, loop=False),
            'kill0/idle': Animation(load_images('entities/kill/0/idle'), img_dur=120, loop=True),
            'kill1/idle': Animation(load_images('entities/kill/1/idle'), img_dur=120, loop=True),
            'kill2/idle': Animation(load_images('entities/kill/2/idle'), img_dur=120, loop=True),
            'kill3/idle': Animation(load_images('entities/kill/3/idle'), img_dur=120, loop=True),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }
        
        self.assets['overlay'].set_alpha(100)
        self.icon = pygame.display.set_icon(self.assets['grassicon'])
        
        self.fonts = {
            'small': Font('small_font.png'),
            'big': Font('large_font.png'),
        }
        
        self.keybinding_rect = self.fonts['big'].render(self.screen, '---   ', (460, 250), scale=[10, 10], colour=(255, 225, 255))
        pygame.display.update()
        
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'spring': pygame.mixer.Sound('data/sfx/spring.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        
        self.music = {
            'base' : pygame.mixer.Sound('data/music.wav')
        }
        self.music['base'].set_volume(0.5)
        
        self.keybinding_rect = self.fonts['big'].render(self.screen, '----  ', (460, 250), scale=[10, 10], colour=(255, 225, 255))
        pygame.display.update()
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        
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
        
        try:
            self.keybinds = self.settings_vals['keybinds']
        except:
            self.keybinds = {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'jump': pygame.K_z,
                'down': pygame.K_DOWN,
                'dash': pygame.K_x,
                'menu': pygame.K_m,
                'respawn': pygame.K_r,
                'restore defaults': 'the gloop'
            }
        self.keybind_defaults = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_UP,
            'down': pygame.K_DOWN,
            'dash': pygame.K_x,
            'menu': pygame.K_m,
            'respawn': pygame.K_r,
            'restore defaults': 'the gloop'
        }
        try:
            self.keybindingvalue = self.settingsval['keybindingvalue']
        except:
            self.keybindingvalue = ['LEFT', 'RIGHT', 'Z', 'X', 'M', 'R', '']
            
        
        self.keybindingname = ['LEFT', 'RIGHT', 'JUMP', 'DASH', 'MENU', 'RESPAWN', 'RESTORE DEFAULTS']
        
        self.keybindingvaluedefault = ['LEFT', 'RIGHT', 'Z', 'X', 'M', 'R', '']
        
        self.col_loop = True
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.camera = "free"
        self.camera_checks = 0
        self.camera_pos = [50, 50]
        self.player = Player(self, (50, 50), (8, 15))
        self.jumpbuf = 0
        self.coyote = 0
        self.dt = 0
        self.tilemap = Tilemap(self, tile_size=16)
        self.layers = ['rooms', 'fgscaled', 'fg', 'mg', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invis']
        self.MM = MusicManager(self)
        self.volume = 100
        self.settings = 'mainpage'
        self.reload_enemies = []
        
        self.save_curr = self.FM.savefile("dump")
        self.respawnpoint = self.save_curr['checkpoint']
        if self.respawnpoint == [0, 0]:
            self.hascheckpoint = 0
        else:
            self.hascheckpoint = 1
        self.level = self.save_curr['level']
        self.load_level(self.level)
        self.render_scroll = [0, 0]
        
        self.checkpointscollected = []
        self.isfullscreen = False
        self.disable_fullscreen_polling = False
        self.screenshake = 0
        self.freezefr = 0
        mpos = [0, 0]
        self.isrenderhb = False
        self.mpos_r = pygame.Rect(mpos[1], mpos[0], 5, 5)
        
        self.settings = 'mainpage'
        self.keybinding_rect = self.fonts['big'].render(self.screen, '-----', (460, 250), scale=[10, 10], colour=(255, 225, 255))
        pygame.display.update()
        
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.tilemap.randomisetiles()
        self.leaf_spawners = []
        
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
        
           
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                if self.hascheckpoint == 1:
                    self.player.pos = self.respawnpoint.copy()
                else:
                    self.player.pos = spawner['pos']
                    self.respawnpoint = self.player.pos
                self.player.air_time = 0
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
        self.reload_enemies = self.enemies.copy()
        
        self.breakable = []
        for breakable in self.tilemap.extract([('breakables', 0)]):
                self.breakable.append(Breakable(self, breakable['pos'], (13, 13)))
                
        
        self.player.velocity = [0, 0]
        self.shards = []
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.checkpointscollected = []
    
        
        self.scroll = [0, 0]
        self.death = []
        self.dead = 0
        self.hascheckpoint = 0
        self.transition = -30
    
    def reload_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.tilemap.randomisetiles()
        
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
           
        self.enemies = self.reload_enemies.copy()
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                if self.hascheckpoint == 1:
                    self.player.pos = self.respawnpoint.copy()
                else:
                    self.player.pos = spawner['pos']
                self.player.air_time = 0
        
        self.breakable = []
        for breakable in self.tilemap.extract([('breakables', 0)]):
                self.breakable.append(Breakable(self, breakable['pos'], (13, 13)))
        
        self.shards = []
        self.death = []
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.player.velocity = [0, 0]
        self.dead = 0
        self.transition = -30
    
    def load_bglevel(self, map_id):
        self.tilemap.load('data/bgmaps/' + str(map_id) + '.json')
        
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
           
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
        
        self.breakable = []
        for breakable in self.tilemap.extract([('breakables', 0)]):
                self.breakable.append(Breakable(self, breakable['pos'], (13, 13)))
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 1
        self.transition = -30
    
    def update_all(self, render_scroll):
        self.clouds.update()
        
        
                    
        for breakable in self.breakable.copy():
            kill = breakable.update(self.tilemap, (0, 0))
            breakable.render(self.display, offset=render_scroll)
            if kill:
                self.breakable.remove(breakable)
                for i in range(0, random.randint(1, 10)):
                    self.shards.append(Shard(self, breakable.pos, (8, 15)))
                    
                    
        for shard in self.shards.copy():
            kill = shard.update(self.tilemap, (0, 0))
            if kill:
                self.shards.remove(shard)
                    
        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0, 0))
            if kill:
                self.enemies.remove(enemy)
                self.death.append(Enemydead(self, enemy.pos, (8, 15)))
                self.freezefr = 20
                    
        for death in self.death.copy():
            kill = death.update(self.tilemap, (0, 0))
            if kill:
                self.death.remove(death)
                    
            
            
        if not self.dead:
            self.player.update(self.tilemap, ((80 * (self.movement[1] - self.movement[0])) * self.dt, 0))
            
            kill = self.player.kill_check(self.tilemap)
            if kill:
                self.dead += 1
                self.sfx['hit'].play()
                self.screenshake = max(32, self.screenshake)
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                    self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
            if self.player.cameratrcollisions == True:
                self.camera = "locked"
             # [[x, y], direction, timer]
            
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    self.projectiles.remove(projectile)
                    self.dead += 1
                    self.sfx['hit'].play()
                    self.screenshake = max(32, self.screenshake)
                    for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                        self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                                
                
                
        if self.freezefr % 5 == 0:
            for spark in self.sparks.copy():
                kill = spark.update()
                if kill:
                    self.sparks.remove(spark)
                
            
    
        for particle in self.particles.copy():
            kill = particle.update()
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)
                
       
            
        self.MM.update()
        
        
    def render_all(self, render_scroll):
        self.clouds.render(self.display_2, offset=render_scroll)
        
        for layer in self.tilemap.tilemap:
            self.tilemap.render(self.display, layer, offset=render_scroll)
                    
        for breakable in self.breakable.copy():
            breakable.render(self.display, offset=render_scroll)
                    
        for shard in self.shards.copy():
            shard.render(self.display, offset=render_scroll)
                    
        for enemy in self.enemies.copy():
            enemy.render(self.display, offset=render_scroll)
                    
        for death in self.death.copy():
            death.render(self.display, offset=render_scroll)
                    
            
            
        if not self.dead:
            self.player.render(self.display, offset=render_scroll)
             # [[x, y], direction, timer]
            
        for projectile in self.projectiles.copy():
            img = self.assets['projectile']
            self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                
        
         
        if self.freezefr % 5 == 0:
            for spark in self.sparks.copy():
                spark.render(self.display, offset=render_scroll)
                
        
        for particle in self.particles.copy():
            particle.render(self.display, offset=render_scroll)
            
        display_mask = pygame.mask.from_surface(self.display)
        display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(display_sillhouette, offset)
    
        
        
        
        
            
        
        
        
    def run(self):
        self.freezefr = 0
        self.camera = "free"
        self.camera_checks = 0
        
        self.MM.fadebetween('base', 'base2', timeinms=1000, goalvolumeout=0.0, goalvolumein=1.0)
        
        
        self.camera_pos = [50, 50]
        self.MM.sfx['ambience'].play(-1)
        self.save_curr = self.FM.savefile("dump")
        if self.respawnpoint == [0, 0]:
            self.hascheckpoint = 0
        else:
            self.hascheckpoint = 1
            self.player.pos = self.respawnpoint.copy()
        self.load_level(self.level)
        self.menu = 'play'
        #if self.isfullscreen:
        #    self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
        #else:
        #    self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.scroll[0] = self.player.rect().centerx
        self.scroll[1] = self.player.rect().centery
        while True:
            if self.freezefr == 0:
                
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))
            
            
                self.screenshake = max(0, self.screenshake - 1)
            
                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        self.hascheckpoint = 0
                        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        self.FM.savefile("save")
                        self.load_level(self.level)
                
                
                
                if self.transition < 0:
                    self.transition += 1
        
                if self.dead:
                    self.dead += 1
                    self.player.lockplayer = True
                    if self.dead >= 10:
                        self.transition = min(60, self.transition + 1)
                    if self.dead > 40:
                        self.reload_level(self.level)
                else:
                    self.player.lockplayer = False
                        
                if self.camera == "free":
                    self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
                    self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
                if self.camera == "locked":
                    self.scroll[0] += (self.camera_pos[0] - self.display.get_width() / 2 - self.scroll[0]) / 10                      
                    self.scroll[1] += (self.camera_pos[1] - self.display.get_height() / 2 - self.scroll[1]) / 10
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                    
                rects = self.tilemap.room_cam_collisions(self.player.pos, self.display)
                i = 0
                self.camera_checks = 0
                for rect in rects:
                    if self.player.rect().colliderect(rect):
                        self.camera = 'locked'
                        self.camera_checks = 1
                        self.camera_pos = [rect.centerx, rect.centery]
                    i += 1
                if self.camera_checks == 0:
                    self.camera = 'free'
                    
                
                
                    
                    
                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                    
                self.update_all(render_scroll)
            self.render_all(render_scroll)
            
                
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / (self.screen.get_width() / self.display_3.get_width()) , mpos[1] / (self.screen.get_height() / self.display_3.get_height()))
            self.pause_button_rect = pygame.Rect(0, 0, 16, 16)
            self.mpos_r.x = mpos[0]
            self.mpos_r.y = mpos[1]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.FM.savefile("save")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == self.keybinds['left']:
                        self.movement[0] = True
                    if event.key == self.keybinds['right']:
                        self.movement[1] = True
                    if event.key == self.keybinds['jump']:
                        self.jumpbuf = 10
                    if event.key == self.keybinds['dash']:
                        self.freezefr = self.player.dash()
                    if event.key == self.keybinds['respawn']:
                        self.dead += 1
                    if event.key == pygame.K_h:
                        self.isrenderhb = not self.isrenderhb
                    if event.key == pygame.K_MINUS:
                        self.volume = max(self.volume - 5, 0)
                    if event.key == pygame.K_EQUALS:
                        self.volume = min(self.volume + 5, 100)
                    if event.key == pygame.K_v:
                        self.MM.fadebetween(musicid2='base', timeinms=1000, goalvolumeout=0.0, goalvolumein=1.0)
                    if event.key == pygame.K_i:
                        self.ab = 10
                    if event.key == pygame.K_o:
                        self.ab = 60
                    if event.key == pygame.K_c:
                        if self.camera == "locked":
                            self.camera = "free"
                        else:
                            self.camera = "locked"
                    if event.key == self.keybinds['menu']:
                        self.FM.savefile("save")
                        self.menu = 'main'
                        self.mainmenu()
                        
                if event.type == pygame.KEYUP:
                    if event.key == self.keybinds['left']:
                        self.movement[0] = False
                    if event.key == self.keybinds['right']:
                        self.movement[1] = False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    collisions = self.mpos_r.colliderect(self.pause_button_rect)
                    if collisions:
                        self.FM.savefile("save")
                        self.mainmenu()
                        self.iterations = 0
                if event.type == pygame.VIDEORESIZE:
                    if not self.isfullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.window_size = [self.screen.get_width(), self.screen.get_height()]
                            
                        self.FM.settings("save")
                            
            if self.jumpbuf > 0:
                self.jumpbuf -= 1
                if self.player.jump():
                    self.sfx['jump'].play()
                    self.jumpbuf = 0
            
            if self.isrenderhb:
                self.tilemap.rendertilehb(self.display, render_scroll)
                
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                #transition_surf.blit(pygame.transform.scale(self.assets['transition_twirl'], (((60 - abs(self.transition)) * abs(self.transition)), ((60 - abs(self.transition)) * abs(self.transition)))), (self.display.get_width() // 2 - ((60 - abs(self.transition)) * abs(self.transition) / 2), self.display.get_height() // 2 - ((60 - abs(self.transition)) * abs(self.transition) / 2)))
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
        
            self.freezefr = max(0, self.freezefr - 1)
            
            
            self.display_2.blit(self.display, (0, 0))
            
            self.fonts['small'].render(self.display_2, 'level ' + str(self.level + 1), [0, 8], [1, 1], (255, 255, 255))
            self.fonts['small'].render(self.display_2, str(round(self.clock.get_fps())) + 'fps', [0, 16], [1, 1], (255, 255, 255))
            self.fonts['small'].render(self.display_2, 'dt:' + str(self.dt), [0, 24], [1, 1], (255, 255, 255))
            self.display_2.blit(self.assets['pause'], (0, 0))
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            
            #self.screen.blit(pygame.transform.gaussian_blur(self.display_2, 5), (0, 0))
            pygame.display.update()
            self.dt = self.clock.tick(60) / 1000
                
                
                
                
                
                
                
                
                
                
                
    
    def mainmenu(self):
        self.menu = 'main'
        
        pygame.mixer.stop()
        
        self.MM.fadebetween('base2', 'base', timeinms=1000, goalvolumeout=0.0, goalvolumein=1.0)
        
        rand = random.randint(0,0)
        self.bglevel = rand
        self.load_bglevel(self.bglevel)
        #self.tile_scroll_anim = self.assets['settings_tile_scroll'].copy()
        self.bg_transition = 0
        self.tile_scroll_pos = 0
        self.iters = 0
        self.keybinding_rect = pygame.Rect(1, 1, 1, 1)
        self.key_rects = []
        self.torender = ' '
        self.key_to_change = ' '
        self.key_store = pygame.K_a
        
        
        while True:
            
            self.display.fill((0, 0, 0, 0))
            
            self.display_3.blit(pygame.transform.gaussian_blur(self.assets['menubackground'], 5), (0, 0))
            
            self.MM.update()
            
            
            
            mpos = pygame.mouse.get_pos()
            self.mpos = (mpos[0] / (self.screen.get_width() / self.display_3.get_width()) , mpos[1] / (self.screen.get_height() / self.display_3.get_height()))
            self.start_button_rect = pygame.Rect(128, 100, 64, 32)
            self.settings_rect = pygame.Rect(128, 136, 64, 32)
            self.return_rect = pygame.Rect(4, 4, 16, 16)
            self.isfullscreen_rect = pygame.Rect(self.display_3.get_width() - 20, 4, 16, 16)
            self.mpos_r.x = self.mpos[0]
            self.mpos_r.y = self.mpos[1]
            
            for breakable in self.breakable.copy():
                kill = breakable.update(self.tilemap,  (0, 0))
                breakable.render(self.display_3,  (math.floor(mpos[0] / 20 + 64), math.floor(mpos[1] / 20 - 25)))
                if kill:
                    self.breakable.remove(breakable)
                    
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_3.blit(display_sillhouette, offset)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    
                    
                                
                    
                    if self.menu == 'main':
                        
                        collisions = self.mpos_r.colliderect(self.start_button_rect)
                        if collisions:
                            self.menu = 'play'
                            self.run()
                        collisions = self.mpos_r.colliderect(self.settings_rect)
                        if collisions:
                            self.menu = 'settings'
                    if self.menu == 'settings':
                        
                        if self.settings == 'mainpage':
                            for button in self.buttons:
                                action = self.buttons[button].update(self.mpos_r)
                                if action:
                                    self.settings = self.buttons[button].action
                    
                
                            collisions = self.mpos_r.colliderect(self.return_rect)
                            if collisions:
                                self.menu = 'main'
                                self.iterations = 0
                            
                            collisions = self.mpos_r.colliderect(self.keybinding_rect)
                            if collisions:
                                self.settings = 'keybinds'
                    
                            collisions = self.mpos_r.colliderect(self.isfullscreen_rect)
                            if collisions:
                                self.isfullscreen = not self.isfullscreen
                                if self.isfullscreen:
                                    self.disable_fullscreen_polling = True
                                    self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                                else:
                                    self.disable_fullscreen_polling = False
                                    self.screen = pygame.display.set_mode(self.base_screen_size, pygame.RESIZABLE)
                            
                        if self.settings == 'soundsliders':
                            for slider in self.sliders:
                                self.sliders[slider].has_grab(self.mpos)
                        
                        elif self.settings == 'screensize':
                            for button in self.resolution_options:
                                action = self.resolution_options[button].update(self.mpos_r)
                                if action:
                                    self.screen = pygame.display.set_mode(self.resolution_options[button].action, pygame.RESIZABLE, vsync=0)
                        
                        if self.settings == 'keybinds':
                            collisions = self.mpos_r.colliderect(self.return_rect)
                            if collisions:
                                self.settings = 'mainpage'
                            
                            for i in range(0, len(self.key_rects)):
                                collisions = self.mpos_r.colliderect(self.key_rects[i])
                                if collisions:
                                    if self.keybindingname[i] == 'RESTORE DEFAULTS':
                                        self.keybinds = self.keybind_defaults.copy()
                                        self.keybindingvalue = self.keybindingvaluedefault.copy()
                                    else:
                                        self.key_to_change = self.keybindingname[i]
                                        self.valtoset = i
                                        self.settings = 'changekey'
                                
                        collisions = self.mpos_r.colliderect(self.return_rect)
                        if collisions:
                            self.settings = self.return_heirarchy[self.settings]
                            
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    for slider in self.sliders:
                        self.sliders[slider].hasgrab = False
                        
                if event.type == pygame.KEYDOWN:
                    if self.settings == 'changekey':
                        if event.key == pygame.K_RETURN:
                            self.FM.settings("save") 
                            self.torender = ' '
                            self.settings = 'keybinds'
                        else:
                            
                            self.keybinds[self.key_to_change.lower()] = event.key
                            self.torender = pygame.key.name(event.key)
                            self.torender = self.torender.upper()
                            self.keybindingvalue[self.valtoset] = self.torender
                    else:
                        if event.key == pygame.K_SPACE:
                            self.menu = 'play'
                            self.run()
                            self.iterations = 0
                        if event.key == pygame.K_f:
                            self.isfullscreen = not self.isfullscreen
                            if self.isfullscreen:
                                self.disable_fullscreen_polling = True
                                self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode(self.base_screen_size, pygame.RESIZABLE)
                                self.disable_fullscreen_polling = False
                        if event.key == pygame.K_d:
                            self.save_curr = self.FM.savefile("clear")
                            self.respawnpoint = self.save_curr["checkpoint"]
                            self.level = self.save_curr["level"]
                if event.type == pygame.VIDEORESIZE:
                    if self.isfullscreen == False:
                        if self.disable_fullscreen_polling == False:
                            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                            self.window_size = [self.screen.get_width(), self.screen.get_height()]
                            
                            self.FM.settings("save")
            
            for slider in self.sliders:
                self.sliders[slider].update(self.mpos)
            
            
            size = self.screen.get_size()
            size = [math.floor(size[0] *  0.40), math.floor(size[1] * 0.40)]
            for layer in self.tilemap.tilemap:
                self.tilemap.render(self.display_3, layer, (math.floor(mpos[0] / 20 + 64), math.floor(mpos[1] / 20 - 25)))
                
                
            self.assets['settingsbg'].set_alpha(self.bg_transition)
            self.display_3.blit(self.assets['settingsbg'], (0, 0))
            if self.iters >= 16:
                self.iters = 0
            for i in range(0, ((int(self.display_3.get_width() / 16) + 2))):
                #self.display_3.blit(img, ((i * 16), (int(self.display.get_height() - 16))))
                self.display_3.blit(self.assets['settings_tile_scroll'], (((i * 16) + self.iters - 16), (int(self.display.get_height() -  self.tile_scroll_pos))))
            for i in range(0, ((int(self.display_3.get_width() / 16) + 2))):
                self.display_3.blit(self.assets['settings_tile_scroll_rev'], (((i * 16) - self.iters - 16),  self.tile_scroll_pos - 16))
            self.iters += 1
            
            
            
            if self.menu == 'settings':
                self.bg_transition = min(self.bg_transition + 5, 200) 
                self.tile_scroll_pos = min(self.tile_scroll_pos + 0.5, 16)
            
                #self.tile_scroll_anim.update()
                #img = self.tile_scroll_anim.img()
                if self.settings == 'mainpage':
                    self.display_3.blit(self.assets['return'], (4, 4))
                    if self.isfullscreen == 0:
                        self.display_3.blit(self.assets['into_fullscreen'], (self.display_3.get_width() - 20, 4))
                    else:
                        self.display_3.blit(self.assets['exit_fullscreen'], (self.display_3.get_width() - 20, 4))
                    
                    
                    #self.keybinding_rect = self.fonts['small'].render(self.display_3, 'KEY BINDINGS', (20, 20), scale=[3, 3], colour=(255, 225, 255))
                    
                    
                    self.buttons['tokeybinds'].render(self.display_3, self.fonts['small'])
                    self.buttons['tosounds'].render(self.display_3, self.fonts['small'])
                    self.buttons['tores_opts'].render(self.display_3, self.fonts['small'])
                    
                elif self.settings == 'keybinds':
                        
                    self.keybinding_rect = self.fonts['big'].render(self.display_3, '- KEYBINDINGS', (20, 16), scale=[1, 1], colour=(255, 225, 255))
                    self.key_rects = []
                    for key in range(0, len(self.keybindingname)):
                        self.key_rects.append(self.fonts['small'].render(self.display_3, self.keybindingname[key], (20, 28 + (key*16)), scale=[2, 2], colour=(255, 225, 255)))
                        
                        self.fonts['small'].render(self.display_3, self.keybindingvalue[key], (180, 28 + (key*16)), scale=[2, 2], colour=(255, 225, 255))
                    
                        
                elif self.settings == 'soundsliders':
                    self.sliders['sfx'].render(self.display_3, self.fonts['small'])
                    
                        
                elif self.settings == 'changekey':
                    self.display_3.blit(self.assets['settingsbg'], (0, 0))
                    
                    self.key_rects.append(self.fonts['small'].render(self.display_3, 'set ' + self.key_to_change.lower() + ' key to', (120, 70), scale=[2, 2], colour=(255, 225, 255)))
                    self.key_rects.append(self.fonts['small'].render(self.display_3, self.torender, (160, 90), scale=[2, 2], colour=(255, 225, 255)))
                    self.key_rects.append(self.fonts['small'].render(self.display_3, 'PRESS ENTER TO CONFIRM', (80, 110), scale=[2, 2], colour=(255, 225, 255)))
                
                elif self.settings == 'screensize':
                    for button in self.resolution_options:
                        self.resolution_options[button].render(self.display_3, self.fonts['small'])
            
                self.display_3.blit(self.assets['return'], (4, 4))
                    
            elif self.menu == 'main':
                self.tile_scroll_pos = max(self.tile_scroll_pos - 0.5, 0)
                self.bg_transition = max(self.bg_transition - 5, 0) 
                #self.display_3.blit(self.assets['testbutton'], (128,100))
                    
                    
                    
                #self.display_3.blit(self.assets['settings'], (128,136))
                    
                if self.col_loop:
                    self.fonts['small'].render(self.display_3, 'START', (131, 107), scale=[3, 3], colour=(15, 225, 200))
                    
                else:
                    self.fonts['small'].render(self.display_3, 'START', (131, 107), scale=[3, 3], colour=(200, 200, 15))
                self.fonts['small'].render(self.display_3, 'SETTINGS', (133, 148), scale=[1.75, 1.75], colour=(255, 255, 255))
                    
            self.screen.blit(pygame.transform.scale(self.display_3, self.screen.get_size()), (0, 0))
            self.col_loop = not self.col_loop
        
                

            pygame.display.update()
            self.clock.tick(60)
            
cProfile.run('Game().mainmenu()')     
#Game().mainmenu()