import json
import random
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1), (1, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (1, -1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (-1, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1)])): 1,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (-1, -1)])): 1,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)])): 1,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (1, -1)])): 1,
    tuple(sorted([(-1, 0), (0, 1), (-1, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (-1, -1)])): 2, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (-1, -1), (1, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (1, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1)])): 3,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (-1, 1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (1, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)])): 5,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (-1, 1)])): 5,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)])): 5,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (1, 1)])): 5,
    tuple(sorted([(1, 0), (0, -1), (1, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (-1, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (-1, -1), (1, 1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (1, 1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1)])): 7,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1)])): 7,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)])): 7,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1)])): 7,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 8,
    tuple(sorted([(-1, 0), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 9,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (1, 1)])): 10,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1)])): 11,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 12,
    tuple(sorted([(1, 0)])): 13,
    tuple(sorted([(1, 0), (1, -1)])): 13,
    tuple(sorted([(1, 0), (1, 1), (1, -1)])): 13,
    tuple(sorted([(1, 0), (1, 1)])): 13,
    tuple(sorted([(1, 0), (-1, 0)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, 1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (1, 1), (1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (1, 1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (1, 1), (1, -1)])): 14,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)])): 14,
    tuple(sorted([(-1, 0)])): 15,
    tuple(sorted([(-1, 0), (-1, -1)])): 15,
    tuple(sorted([(-1, 0), (-1, 1), (-1, -1)])): 15,
    tuple(sorted([(-1, 0), (-1, 1)])): 15,
}
AUTOTILE_MAP2 = {   
    tuple(sorted([(1, 0), (0, 1), (1, 1)])): 16,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (1, -1)])): 16,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1)])): 16,
    tuple(sorted([(1, 0), (0, 1), (1, 1), (-1, 1)])): 16,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1)])): 17,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (-1, -1)])): 17,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)])): 17,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (-1, 1), (1, 1), (1, -1)])): 17,
    tuple(sorted([(-1, 0), (0, 1), (-1, 1)])): 18, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (-1, -1)])): 18, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (-1, -1), (1, 1)])): 18, 
    tuple(sorted([(-1, 0), (0, 1), (-1, 1), (1, 1)])): 18, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)])): 19,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1)])): 19,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])): 19,
    tuple(sorted([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1)])): 19,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1)])): 20,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (-1, 1)])): 20,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)])): 20,
    tuple(sorted([(-1, 0), (0, -1), (-1, -1), (1, -1)])): 20,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1)])): 21,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (-1, 1)])): 21,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)])): 21,
    tuple(sorted([(-1, 0), (0, -1), (1, 0), (-1, -1), (1, -1), (1, 1)])): 21,
    tuple(sorted([(1, 0), (0, -1), (1, -1)])): 22,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (-1, -1)])): 22,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (-1, -1), (1, 1)])): 22,
    tuple(sorted([(1, 0), (0, -1), (1, -1), (1, 1)])): 22,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1)])): 23,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1)])): 23,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)])): 23,
    tuple(sorted([(1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1)])): 23,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 24,
    tuple(sorted([(-1, 0), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 25,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (1, 1)])): 26,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1)])): 27,
    tuple(sorted([(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)])): 28,
    tuple(sorted([(1, 0)])): 29,
    tuple(sorted([(1, 0), (1, -1)])): 29,
    tuple(sorted([(1, 0), (1, 1), (1, -1)])): 29,
    tuple(sorted([(1, 0), (1, 1)])): 29,
    tuple(sorted([(1, 0), (-1, 0)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, 1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (1, 1), (1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (1, 1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (1, 1), (1, -1)])): 30,
    tuple(sorted([(1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)])): 30,
    tuple(sorted([(-1, 0)])): 31,
    tuple(sorted([(-1, 0), (-1, -1)])): 31,
    tuple(sorted([(-1, 0), (-1, 1), (-1, -1)])): 31,
    tuple(sorted([(-1, 0), (-1, 1)])): 31,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone', 'ice'}
KILL_TILES = {'kill', 'killbricks'}
MOVEMENT_TILES = {'bouncepad'}
CHECKPOINT_TILES = {'checkpoint'}
CAMERA_TRIGGER_TILES = {'cameratr'}
BREAKABLES_TILES = {'breakables'}
AUTOTILE_TYPES = {'grass', 'stone', 'ice', 'base'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def trigger_rects_around(self, pos):
        rects = []
        variants = []
        for tile in self.tiles_around(pos):
            if tile['type'] in CAMERA_TRIGGER_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
                variants.append(tile['variant'])
        return [rects, variants]
    
    def kill_rects_around(self, pos):
        rects = []
        for tile in self.offgrid_tiles:
            if tile['type'] in KILL_TILES:
                if tile['type'] == 'killbricks':
                    rects.append(pygame.Rect(tile['pos'][0], tile['pos'][1], self.tile_size, self.tile_size))
                elif tile['type'] == 'kill':
                    rects.append(pygame.Rect(tile['pos'][0] + 3, tile['pos'][1]+ 3, self.tile_size - 6, self.tile_size - 6))
        for tile in self.tiles_around(pos):
            if tile['type'] in KILL_TILES:
                if tile['type'] == 'killbricks':
                    rects.append(pygame.Rect(tile['pos'][0] * self.tile_size + 3, tile['pos'][1] * self.tile_size + 3, self.tile_size - 6, self.tile_size - 6))
                elif tile['type'] == 'kill':
                    rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def movement_rects_around(self, pos):
        rects = []
        for tile in self.offgrid_tiles:
            if tile['type'] in MOVEMENT_TILES:
               rects.append(pygame.Rect(tile['pos'][0] + 3, tile['pos'][1], self.tile_size, self.tile_size))
        for tile in self.tiles_around(pos):
            if tile['type'] in MOVEMENT_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def rendertilehb(self, surf, offset=(0, 0)):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in KILL_TILES:
                pygame.draw.rect(surf, (255, 0, 0), (tile['pos'][0] * self.tile_size - offset[0] + 3, tile['pos'][1] * self.tile_size - offset[1] + 3, self.tile_size - 6, self.tile_size - 6), 1)
            elif tile['type'] in PHYSICS_TILES:
                pygame.draw.rect(surf, (100, 0, 0), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1], self.tile_size, self.tile_size), 1)
            elif tile['type'] in CHECKPOINT_TILES:
                pygame.draw.rect(surf, (0, 100, 0), (tile['pos'][0] * self.tile_size - offset[0] - 2, tile['pos'][1] * self.tile_size - offset[1] - 2, 20, 36), 1)
            elif tile['type'] in MOVEMENT_TILES:
                pygame.draw.rect(surf, (0, 100, 100), (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1], self.tile_size, self.tile_size), 1)
        for tile in self.offgrid_tiles:
            if tile['type'] in KILL_TILES:
                pygame.draw.rect(surf, (255, 0, 0), (tile['pos'][0] - offset[0] + 3, tile['pos'][1] - offset[1] + 3, self.tile_size - 6, self.tile_size - 6), 1)
            elif tile['type'] in PHYSICS_TILES:
                pygame.draw.rect(surf, (100, 0, 0), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1], self.tile_size, self.tile_size), 1)
            elif tile['type'] in CHECKPOINT_TILES:
                pygame.draw.rect(surf, (0, 100, 0), (tile['pos'][0] - offset[0] - 2, tile['pos'][1] - offset[1] - 2, 20, 36), 1)
            elif tile['type'] in MOVEMENT_TILES:
                pygame.draw.rect(surf, (0, 100, 100), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1], self.tile_size, self.tile_size), 1)
                
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] in AUTOTILE_TYPES:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if neighbors == [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                tile['variant'] = 10
            elif (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                    tile['variant'] = AUTOTILE_MAP[neighbors]
    
    def show_cam_bounds(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            if tile['type'] == 'cameratr' and tile['variant'] == 2:
                pygame.draw.rect(surf, (255, 200, 50), (tile['pos'][0] - surf.get_width()/ 2 - offset[0], tile['pos'][1] - surf.get_height()/ 2 - offset[1], surf.get_width(), surf.get_height()), 3)
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] == 'cameratr' and tile['variant'] == 2:
                pygame.draw.rect(surf, (255, 200, 50), (tile['pos'][0] * 16 - surf.get_width()/ 2 - offset[0], tile['pos'][1] * 16 - surf.get_height()/ 2 - offset[1], surf.get_width(), surf.get_height()), 3)
                
    def room_cam_collisions(self, pos, surf):
        rects = []
        for tile in self.offgrid_tiles:
            if tile['type'] in CAMERA_TRIGGER_TILES and tile['variant'] == 2:
                rects.append(pygame.Rect((tile['pos'][0]) - surf.get_width()/ 2, (tile['pos'][1]) - surf.get_height()/ 2, surf.get_width(), surf.get_height()))
                
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in CAMERA_TRIGGER_TILES and tile['variant'] == 2:
                rects.append(pygame.Rect((tile['pos'][0] * 16) - surf.get_width()/ 2, (tile['pos'][1] * 16) - surf.get_height()/ 2, surf.get_width(), surf.get_height()))
        return rects
    
    def checkpointcollisions(self, pos, surf):
        rects = []
        for tile in self.offgrid_tiles:
            if tile['type'] in CHECKPOINT_TILES:
                rects.append(pygame.Rect((tile['pos'][0] - 2), (tile['pos'][1] - 2), 20, 36))
                
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in CHECKPOINT_TILES:
                rects.append(pygame.Rect((tile['pos'][0] * 16) - 2, (tile['pos'][1] * 16) - 2, 20, 36))
        return rects
    
    def randomisetiles(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] in PHYSICS_TILES:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            ran = random.choice((1, 0))
            if ran == 1:
                if neighbors == [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                    tile['variant'] = 10
                if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                    tile['variant'] = AUTOTILE_MAP[neighbors]
            else:
                if neighbors == [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                    tile['variant'] = 25
                if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP2):
                    tile['variant'] = AUTOTILE_MAP2[neighbors]
                    
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
        for x in range((offset[0] // self.tile_size) - 2, (offset[0] + surf.get_width()) // self.tile_size + 2):
            for y in range((offset[1] // self.tile_size) - 2, (offset[1] + surf.get_height()) // self.tile_size + 2):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))