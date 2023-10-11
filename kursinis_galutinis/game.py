import pygame
import sys
# import math
from pygame.locals import *
from scripts.tilemap import Map 
from scripts.enemy import Enemy 
from scripts.coin import Coin
from scripts.player import Player
from scripts.button import Button

# BLACK = (0, 0, 0)



screen_width = 640
screen_height = 480



class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Pygame Platformer')


        #FONT

        self.font_size = 30
        self.coin_font = pygame.font.SysFont('ttf', self.font_size)
        self.font = pygame.font.SysFont('ttf',self.font_size)
        self.color = (255, 215, 0)
        
        self.game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        self.game_won_text = self.font.render('Game Won', True, (255, 0, 0)) 

        #WINDOW/DISPLAY

        self.WINDOW_SIZE = (1280, 960)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        self.display = pygame.Surface((640, 480)) #turi buti sumazintas
        self.clock = pygame.time.Clock()
        
        #IMAGES

        self.background_img = pygame.image.load('data/background.png')
        self.grass_img = pygame.image.load('data/grass.png')
        self.dirt_img = pygame.image.load('data/dirt.png')
        self.restart_img = pygame.image.load('data/restart_btn.png')
        self.start_img = pygame.image.load('data/start_btn.png')
        self.exit_img = pygame.image.load('data/exit_btn.png')
        self.image_right = pygame.image.load('data/player_right.png')
        self.image_left = pygame.image.load('data/player_left.png')

        #BUTTONS


        self.start_button = Button(screen_width // 2 - 300, screen_height // 2, self.start_img)
        self.exit_button = Button(screen_width // 2 + 50, screen_height // 2, self.exit_img)

        # GAME SETTINGS

        self.game_state = 'ACTIVE'
        
        self.main_menu = True

        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0
        self.last_collision_time = 0

        
        self.map = Map()
        self.map.load_map('map')

        self.enemy_tile = '3'
        self.coin_tile = '4'

        self.player_img = pygame.image.load('data/player_right.png').convert()
        self.player_img.set_colorkey((0, 0, 0))

        self.player_rect = pygame.Rect(100, 400, 5, 13)

        #GAME RULES
        
        self.player = Player()  
        self.player_won = 5
        self.player_score = 0
        self.player_lives = 5
        self.collected_coins = 0


        # COIN AND ENEMY 


        self.coin_group = pygame.sprite.Group()
        for y, row in enumerate(self.map.game_map):
            for x, tile in enumerate(row):
                if tile == '4':
                    coin = Coin(x * 16, y * 16)
                    self.coin_group.add(coin)

        self.enemies = pygame.sprite.Group()
        for y, row in enumerate(self.map.game_map):
            for x, tile in enumerate(row):
                if tile == '3':
                    enemy = Enemy(x * 16, y * 16 - 2)
                    self.enemies.add(enemy)
                    

        
        # COLLISION

    def collision_test(self, rect, tiles, ignore_tiles=None):
        if ignore_tiles is None:
            ignore_tiles = []

        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile) and tile not in ignore_tiles:
                hit_list.append(tile)

        return hit_list

    
    
        # TEXT

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def render_player_lives(self):
        lives_text = self.font.render(f'LIVES: {self.player_lives}', True, self.color)
        self.display.blit(lives_text, (20, 55))

    def render_collected_coins(self):
        coin_text = self.coin_font.render(f'COINS: {self.collected_coins} / {self.player_won}', True, self.color)
        self.display.blit(coin_text, (20, 18))
        
        # GAME OVER 

    def game_over(self):
        self.game_state = 'GAME_OVER'
        self.game_won_timer = pygame.time.get_ticks()
        
        while True:
       
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.game_won_timer) / 1000  

            if elapsed_time >= 3:  
                self.game_state = 'GAME_OVER'  
                break

        pygame.display.update() 

        print('Zaidimas Baigtas')

        #GAME WON

    def game_won(self):
        self.game_state = 'GAME_WON'
        
        self.draw_text('Sveikinu , laimėjote', self.font, self.color, (screen_width // 2) + 20, screen_height // 2)
        pygame.display.update() 

        print('zaidimas laimetas')

        #MOVEMENT AND COLLISION X and Y 

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True

        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types
    

    #GAME RUN

    def run(self): 
        
        tile_rects = []
         

        while self.game_state == 'ACTIVE':  #GAME LOOP

            self.game_started = False  

          
            self.display.blit(self.background_img, (0, 0)) 
     

            self.display.blit(self.player_img, (self.player_rect.x , self.player_rect.y ))

            
            self.current_time = pygame.time.get_ticks()


            #UPDATE

            self.coin_group.update()
            
            self.player.update(tile_rects)

            self.render_player_lives()  

            self.coin_group.draw(self.display)

            self.enemies.draw(self.display)


            #MOVEMENT
            
            self.player.handle_input()

        
            player_movement = [0, 0]
            if self.moving_right:
                player_movement[0] += 2
            if self.moving_left:
                player_movement[0] -= 2
         
            player_movement[1] += self.vertical_momentum
            self.vertical_momentum += 0.2
            if self.vertical_momentum > 3:
                self.vertical_momentum = 3

            self.player_rect, collisions = self.move(self.player_rect, player_movement, tile_rects)

            if collisions['bottom']:
                self.air_timer = 0
                self.vertical_momentum = 0
            else:
                self.air_timer += 1

           
           #COLLISION WITH ENEMY  
            if self.current_time - self.last_collision_time >= 1500:
                for enemy in self.enemies:
                    enemy.update()
                    if self.player_rect.colliderect(enemy.rect):
                        self.player_lives -= 1
                        self.last_collision_time = self.current_time  
                        print('-1 gyvybe')
                        
                if self.player_lives <= 0:
                    self.draw_text('Žaidimas Baigtas', self.font, self.color, (screen_width // 2) + 20, screen_height // 2)
                    self.game_over()
                    
                

            #COLLISION WITH COIN

            for coin in self.coin_group:
                if self.player_rect.colliderect(coin.rect):
                    self.player_score += 1
                    self.coin_group.remove(coin)
                    self.collected_coins += 1

                if self.collected_coins >= self.player_won:
                    self.game_won()
            
            self.render_collected_coins()
       

            #TILES 

            tile_rects = []
            y = 0
            for layer in self.map.game_map:
                x = 0
                for tile in layer:
                    if tile == '1':
                        self.display.blit(self.dirt_img, (x * 16 , y * 16 ))
                    elif tile == '2':
                        self.display.blit(self.grass_img, (x * 16 , y * 16 ))
                    if tile != '0':
                        tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                    x += 1
                y += 1
            
            self.colliding_tiles = self.collision_test(self.player_rect, tile_rects, ignore_tiles=[self.enemy_tile, self.coin_tile])
            
            #MENU 

            # if self.main_menu:
            #     self.start_button.draw(self.display)  
            #     self.exit_button.draw(self.display)   
               
            #     if self.start_button.clicked:
            #         self.main_menu = False
            #     elif self.exit_button.clicked:
            #         pygame.quit()
            #         sys.exit()
            # if self.start_button.clicked:
            #                 self.main_menu = False


            #KEYBOARD PRESSED & EXIT 
            for event in pygame.event.get():  
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.moving_right = True
                    if event.key == K_LEFT:
                        self.moving_left = True
                    if event.key == K_UP:
                        if self.air_timer < 6:
                            self.vertical_momentum = -5
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        self.moving_right = False
                    if event.key == K_LEFT:
                        self.moving_left = False


            #DISPLAY/SCREEN UPDATE

            self.screen.blit(pygame.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            
            

if __name__ == "__main__":
    game = Game()
    game.run()
