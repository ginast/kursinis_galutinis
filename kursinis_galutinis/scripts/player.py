import pygame
from pygame.locals import *

class Player:
    def __init__(self):
        self.image_right = pygame.image.load('data/player_right.png').convert()
        self.image_left = pygame.image.load('data/player_left.png').convert()
        self.image = self.image_left

        self.image.set_colorkey((0, 0, 0))
    
        self.vertical_momentum = 0

    def handle_input(self):

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.image = self.image_right
           
            # print("Moving right")
        if keys[K_LEFT]:
            self.image = self.image_left
   
            # print("Moving left")
        if keys[K_UP]:
            if self.on_ground():  
                self.vertical_momentum = -3

    def on_ground(self):
       
        pass

    def update(self, tile_rects):
      pass