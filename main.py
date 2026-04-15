import pygame 
import time, random
import sys
from pygame.locals import *
import sprites

def main():
    pygame.init()

    FPS = 60
    FramePerSec = pygame.time.Clock()

    font = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 20)
    game_over = font.render("Game Over", True, sprites.BLACK)

    background = pygame.image.load("assets/Road.png")
    background = pygame.transform.scale(background, (400, 600))

    SCREEN = pygame.display.set_mode((sprites.WIDTH, sprites.HEIGHT))
    SCREEN.fill(sprites.WHITE)
    pygame.display.set_caption("Racer")
            
    P1 = sprites.Player()
    E1 = sprites.Enemy()
    C = sprites.Coin()

    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies.add(E1)
    coins.add(C)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                sprites.SPEED += 0.5
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        SCREEN.blit(background, (0, 0))
        scores = font_small.render("SCORES:  " + str(sprites.SCORE), True, sprites.GREEN)        
        SCREEN.blit(scores, (10, 10))
        
        for entity in all_sprites:
            SCREEN.blit(entity.image, entity.rect)
            entity.move()
            
        for coin in coins:
            SCREEN.blit(coin.image, coin.rect)
            
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound('assets/accident.mp3').play()
            time.sleep(0.5)
            
            SCREEN.fill(sprites.RED)
            SCREEN.blit(game_over, (30, 250))
            
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            
            time.sleep(2)
            pygame.quit()
            sys.exit()
            
        if pygame.sprite.spritecollideany(P1, coins):
            sprites.SCORE += 1
            pygame.mixer.Sound('assets/coin_taken.wav').play()
            for coin in coins:
                coin.rect.center = (random.randint(40, sprites.WIDTH - 40), 500)

                while pygame.sprite.collide_rect(coin, P1):
                    coin.rect.center = (random.randint(40, sprites.WIDTH - 40), 500)
        
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
    