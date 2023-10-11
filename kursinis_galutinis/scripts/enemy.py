import pygame
import random

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('data/enemy.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.move_direction = random.choice([-1, 1])

		self.move_counter = 0

		self.change_direction_interval = random.randint(50, 150)
		

	def update(self):
		
		self.collided = True 
		
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 25:
			self.move_direction *= -1
			self.move_counter *= -1
