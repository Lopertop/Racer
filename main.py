import pygame 
import time
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

    enemies = pygame.sprite.Group()
    enemies.add(E1)
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
        
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
