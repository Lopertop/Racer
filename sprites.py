import pygame
from pygame.locals import *
import random
    
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0   
GOAL = 5000
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.local_speed = random.randint(2, 5)
        self.spawn()
        
    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), -100)
        
    def move(self):
        self.rect.move_ip(0, SPEED + self.local_speed)
        if self.rect.bottom > HEIGHT:
            self.spawn()
            self.local_speed = random.randint(2, 5)
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
        self.slow_until = 0
        self.has_shield = False
        self.nitro_until = 0
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if current_time < self.nitro_until:
            move_speed = 8
        elif current_time < self.slow_until:
            move_speed = 2
        else:
            move_speed = 5
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-move_speed, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(move_speed, 0)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -move_speed)
        if self.rect.bottom < HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, move_speed)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn()  
        
    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), random.randint(-100, 400))
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect. top > HEIGHT:
            self.spawn()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type='barrier'):
        super().__init__()
        self.type = obstacle_type
        if obstacle_type == "barrier":
            self.image = pygame.image.load("assets/barrier.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 40))
        else:
            self.image = pygame.image.load("assets/spill.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 30))
        
        self.rect = self.image.get_rect()
        self.spawn() 
        
    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), -random.randint(200, 800))
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.spawn()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type=None):
        super().__init__()
        self.type = power_up_type if power_up_type else random.choice(['nitro', 'shield', 'repair'])
        
        if self.type == "nitro":
            self.image = pygame.image.load("assets/nitro.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
        elif self.type == "shield":
            self.image = pygame.image.load("assets/shield.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
        elif self.type == "repair":
            self.image = pygame.image.load("assets/repair.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            
        self.rect = self.image.get_rect()
        self.spawn_time = pygame.time.get_ticks()
        self.spawn()
        
    def spawn(self):
        self.rect.center = (random.randint(40, 400 - 40), -50)
    
    def move(self):
        self.rect.move_ip(0, 5)
        if pygame.time.get_ticks() - self.spawn_time > 7000 or self.rect.top > 600:
            self.kill()