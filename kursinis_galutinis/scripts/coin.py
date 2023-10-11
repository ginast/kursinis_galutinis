import pygame
import random


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/coin.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       
      
        self.move_direction = random.choice([-1, 1])  
     
        self.move_counter = 0
        self.change_direction_interval = random.randint(50, 150)  
        
    def update(self):
        
        self.collided = True 

        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1
            self.move_counter *= -1
		

		
		
		
		
		


       