import math
import random

import pygame

from scripts.particle import Particle
from scripts.musicmanager import SoundSource
from scripts.spark import Spark

#self.game.sfx['shoot'].set_volume(self.game.sfx['shoot'].get_volume() * (min(0, 100-math.dist(self.pos, self.game.player.pos) / 100)))
#self.game.sfx['shoot'].play()

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.imgscaling = [0, 0]
        self.wantscale = [0, 0]
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        
        self.last_movement = [0, 0]
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def nearrect(self):
        return pygame.Rect(self.pos[0] - 4, self.pos[1] - 4, self.size[0] + 8, self.size[1] + 4)
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
    def handlescaling(self):
        if self.imgscaling[0] > self.wantscale[0]:
            #lower val
            #math.floor(self.wantscale[0] / 30)
            self.imgscaling[0] -= max(0.1, self.wantscale[0] * 3)
        elif self.imgscaling[0] < self.wantscale[0]:
            #increase val
            self.imgscaling[0] += max(0.1, self.wantscale[0] * 3)
        if self.imgscaling[1] > self.wantscale[1]:
            #lower val
            self.imgscaling[1] -= max(0.1, self.wantscale[1] / 3)
        elif self.imgscaling[1] < self.wantscale[1]:
            #increase val
            self.imgscaling[1] += max(0.1, self.wantscale[1] / 3)
        
    def update(self, tilemap, movement=(0, 0), iswallsliding=False):
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.nearcollisions = {'right': False, 'left': False}
        self.killcollisions = False
        self.frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += self.frame_movement[0]
        if not iswallsliding:
            entity_rect = self.rect()
            for rect in tilemap.physics_rects_around(self.pos):
                if entity_rect.colliderect(rect):
                    if self.frame_movement[0] > 0:
                        entity_rect.right = rect.left
                        self.collisions['right'] = True
                    if self.frame_movement[0] < 0:
                        entity_rect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entity_rect.x
        
        
        else:
            entity_rect = self.nearrect()
            true_rect = self.rect()
            for rect in tilemap.physics_rects_around(self.pos):
                if entity_rect.colliderect(rect):
                    if self.frame_movement[0] > 0:
                        true_rect.right = rect.left
                        self.collisions['right'] = True
                    if self.frame_movement[0] < 0:
                        true_rect.left = rect.right
                        self.collisions['left'] = True
                    self.pos[0] = entity_rect.x
        
          
        self.pos[1] += self.frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if self.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        for rect in tilemap.kill_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                self.killcollisions = True
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        self.last_collisions = self.collisions
        self.velocity[1] = min(5, self.velocity[1] + 0.125)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.handlescaling()
        self.animation.update()
        
    
        
    def render(self, surf, scale=[0, 0],offset=(0, 0)):
        img = self.animation.img()
        imgsize = img.get_size()
        
        setscale = (imgsize[0] + scale[0], imgsize[1] + scale[1])
        self.imgscaled = pygame.transform.scale(self.animation.img(), setscale)
        surf.blit(pygame.transform.flip(self.imgscaled, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        if self.game.isrenderhb == True:
            self.renderhb(surf, offset)
        
        
    def renderhb(self, surf, offset=(0, 0)):
        if self.type == 'enemy':
            pygame.draw.rect(surf, (255, 0, 0), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]), self.size[0], self.size[1]), 1)
        elif self.type == 'player':
            pygame.draw.rect(surf, (100, 255, 100), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]), self.size[0], self.size[1]), 1)
            pygame.draw.rect(surf, (100, 255, 100), (int(self.pos[0] - offset[0] - 2), int(self.pos[1] - offset[1] - 2), self.size[0] + 4, self.size[1] + 4), 1)
        else:
            pygame.draw.rect(surf, (0, 0, 200), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]), self.size[0], self.size[1]), 1)
        
class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.ss = SoundSource(pygame.mixer.Sound('data/sfx/shoot.wav'), self.pos, 1, 100)
        self.walking = 0
        
    def update(self, tilemap, movement=(0, 0)):
        self.ss.update(self.game.player.pos, self.pos)
        
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.ss.play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.ss.play()
                        #prevol = self.game.sfx['shoot'].get_volume()
                        #self.game.sfx['shoot'].set_volume(self.game.sfx['shoot'].get_volume() * (min(0, 100-math.dist(self.pos, self.game.player.pos) / 100)))
                        #self.game.sfx['shoot'].play()
                        #self.game.sfx['shoot'].set_volume(prevol)
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
        
        
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                self.game.particles.append(Particle(self.game, 'hit', self.rect().center, velocity=[0, 0], frame=0))
                for i in range(30):
                    
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

                
class Breakable(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'breakable', pos, size)
        
    def update(self, tilemap, movement=(0, 0)):
        
        super().update(tilemap, movement=movement)
        
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(12, self.game.screenshake)
                self.game.sfx['hit'].play()
   

                return True
        self.set_action('idle')
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

class Shard(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.once = 0
        self.timer = random.randint(100, 140)
        type = random.randint(0, 2)
        asset = ""
        if type == 0:
            asset = 'breakablea'
        if type == 1:
            asset = 'breakableb'
        if type == 2:
            asset = 'breakablec'
        self.speed = [random.uniform(-4, 4), -20]
        super().__init__(game, asset, pos, size)
    def update(self, tilemap, movement=(0, 0)):
        
        
        super().update(tilemap, movement=movement)
        self.timer -= 1
        if self.once == 0:
            self.set_action('idle')
        
        if self.speed[0] > 0:
            self.speed[0] -= 0.1
        elif self.speed[0] < 0:
            self.speed[0] += 0.1
        self.velocity[0] = self.speed[0]
        if self.timer <= 0:
            return True
        if abs(self.game.player.dashing) >= 50 and self.timer <= 90:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(8, self.game.screenshake)
                if self.speed[0] > 0:
                    self.speed[0] += 2
                elif self.speed[0] < 0:
                    self.speed[0] -= 2
                self.timer += 20
                self.game.sfx['hit'].play()
        if abs(self.game.player.dashing) <= 50 and self.timer <= 90:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(1, self.game.screenshake)
                if self.speed[0] > 0:
                    self.speed[0] += 1
                elif self.speed[0] < 0:
                    self.speed[0] -= 1
                self.timer += 20
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

            
        
        
        
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
class Enemydead(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.once = 0
        self.timer = 120
        type = random.randint(0, 2)
        asset = ""
        if type == 0:
            asset = 'deada'
        if type == 1:
            asset = 'deadb'
        if type == 2:
            asset = 'deadc'
        super().__init__(game, asset, pos, size)
        self.speed = [((self.game.player.velocity[0] / 2) + 1) * 2, random.uniform(-2, -5)]
        
        
    def update(self, tilemap, movement=(0, 0)):
        
        
        super().update(tilemap, movement=movement)
        if self.collisions['left'] or self.collisions['right']:
            self.speed[0] = (self.speed[0] * -1) * 0.8
        self.timer -= 1
        if self.once == 0:
            self.set_action('idle')
        
        if self.speed[0] > 0:
            self.speed[0] -= 0.1
        elif self.speed[0] < 0:
            self.speed[0] += 0.1
        self.speed[1] += 0.1
        self.velocity = self.speed
        if self.timer <= 0:
            return True
        if abs(self.game.player.dashing) >= 50 and self.timer <= 90:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(8, self.game.screenshake)
                if self.speed[0] > 0:
                    self.speed[0] += 2
                elif self.speed[0] < 0:
                    self.speed[0] -= 2
                self.game.sfx['hit'].play()
        if abs(self.game.player.dashing) <= 50 and self.timer <= 90:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(1, self.game.screenshake)
                if self.speed[0] > 0:
                    self.speed[0] += 1
                elif self.speed[0] < 0:
                    self.speed[0] -= 1
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)