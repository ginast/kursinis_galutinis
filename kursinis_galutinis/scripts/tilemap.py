import pygame
from scripts.enemy import Enemy

class Map:
    def __init__(self):
        self.tile_size = 16 

     
    def load_map(self, path):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        self.game_map = []
        for row in data:
            self.game_map.append(list(row))
    
    