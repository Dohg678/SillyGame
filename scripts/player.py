import math
import random
import pygame

from scripts.particle import Particle
from scripts.spark import Spark
        
    
    
        
        
        
        
    



class Player():
    def __init__(self, game, pos, size):
        self.game = game
        self.type = 'player'
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
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.isspark = 0
        self.coyote = 0
        self.stamina = 20
        self.cameratrcollisions = False
        self.lockplayer = False
        self.last_collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        

    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.nearcollisions = {'right': False, 'left': False}
        self.killcollisions = False
        self.frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        if not self.lockplayer:
            self.pos[0] += self.frame_movement[0]
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
        
        
        #    entity_rect = self.nearrect()
         #   true_rect = self.rect()
          #  for rect in tilemap.physics_rects_around(self.pos):
           #     if entity_rect.colliderect(rect):
            ##        if self.frame_movement[0] > 0:
              #          true_rect.right = rect.left
               #         self.collisions['right'] = True
                #    if self.frame_movement[0] < 0:
                 #       true_rect.left = rect.right
                  #      self.collisions['left'] = True
                   # self.pos[0] = entity_rect.x
        if not self.lockplayer:
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
        
        self.velocity[1] = min(5, self.velocity[1] + (6.5 * self.game.dt))
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        if self.air_time > 4 and self.collisions['down']:
            self.game.screenshake += self.air_time / 5
            self.game.particles.append(Particle(self.game, 'impactdust', [self.rect().left, self.rect().bottom], velocity=[0, 0], frame=random.randint(0, 7)))
            
        self.handlescaling()
        self.animation.update()
        
        self.cameratrcollisions = False
        entity_rect = self.rect()
        rects, variant = tilemap.trigger_rects_around(self.pos)
        i = 0
        for rect in rects:
            if entity_rect.colliderect(rect):
                
                if variant[i] == 0:
                    self.game.camera = "locked"
                elif variant[i] == 1:
                    self.game.camera = "free"
                i += 1  
                      
        for rect in tilemap.movement_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                self.velocity[1] = -3
                self.jumps = 0
                self.air_time = 0
                self.game.sfx['spring'].play()
        
        
        for rect in tilemap.checkpointcollisions(self.pos, self.game.display):
            if self.rect().colliderect(rect):
                if not [rect.centerx, rect.centery] in self.game.checkpointscollected:
                    self.game.hascheckpoint = 1
                    self.game.checkpointscollected.append([rect.centerx, rect.centery])
                    self.game.reload_enemies = self.game.enemies.copy()
                    self.game.respawnpoint = [rect.centerx, rect.centery]
                   
        
        self.isspark += 1
        self.air_time += 1
        
        if self.killcollisions:
            self.game.dead += 1
            
        if self.air_time > 180:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1
        
        if self.game.dead > 0:
            self.dashing = 0
            self.velocity = [0, 0]
            
        if self.collisions['down']:
            
            self.air_time = 0
            self.jumps = 1
            self.coyote = 10
            self.imgscaling = [0, 0]
        else:
            self.coyote -= 1
            
        if self.coyote == 0:
            self.jumps = 0
            
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.stamina -= 1
            self.air_time = 4
            self.velocity[1] = min(self.velocity[1], 0)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
                if self.isspark == 20:
                    if not self.flip:
                        self.game.particles.append(Particle(self.game, 'walkdust', [self.rect().left, self.rect().bottom], velocity=[0, -0.2], frame=random.randint(0, 7)))
                    else:
                        self.game.particles.append(Particle(self.game, 'walkdust', [self.rect().right, self.rect().bottom], velocity=[0, -0.2], frame=random.randint(0, 7)))
                    self.isspark = 0
            else:
                self.set_action('idle')
        
        if self.isspark == 20:
            self.isspark = 0
        
        if abs(self.dashing) in {60, 50}:
            if self.velocity[1] < 0:
                self.velocity[1] = 0
                
            for i in range(20):
                
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        
        self.wantscale[1] = abs(self.velocity[1] * 3)
        if self.velocity[1] > 1:
            self.wantscale[0] = (abs(self.velocity[1]) * -1)
            
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
        
        
        self.last_collisions = self.collisions
    
    def render(self, surf, offset=(0, 0), scale=[0, 0]):
        if abs(self.dashing) <= 50:
            img = self.animation.img()
            imgsize = img.get_size()
        
            setscale = (imgsize[0] + scale[0], imgsize[1] + scale[1])
            self.imgscaled = pygame.transform.scale(self.animation.img(), setscale)
            surf.blit(pygame.transform.flip(self.imgscaled, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
            if self.game.isrenderhb == True:
                self.renderhb(surf, offset)
            
    def jump(self):
        if self.wall_slide:
            self.wantscale = [-2, 3]
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = max(3.5, self.velocity[0] + 3.5)
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = min(-3.5, self.velocity[0] - 3.5)
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.wantscale = [-2, 3]
            self.velocity[1] = -2.75
            self.jumps -= 1
            self.air_time = 5
            return True
        
    def kill_check(self, tilemap):
        entity_rect = self.rect()
        for rect in tilemap.kill_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                return True
    
    def dash(self):
        #if not self.dashing:
            self.game.sfx['dash'].play()
            self.game.screenshake = 16
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
            return 4
        #else:
            #return 0
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def nearrect(self):
        return pygame.Rect(self.pos[0] - 4, self.pos[1] - 4, self.size[0] + 8, self.size[1] + 8)
    
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
        
    def renderhb(self, surf, offset=(0, 0)):
        pygame.draw.rect(surf, (100, 255, 100), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]), self.size[0], self.size[1]), 1)
        pygame.draw.rect(surf, (100, 255, 100), (int(self.pos[0] - offset[0] - 4), int(self.pos[1] - offset[1] - 4), self.size[0] + 8, self.size[1] + 8), 1)
