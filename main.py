import pygame 
import time, random
import sys
from pygame.locals import *
import sprites
import json
import os

def load_leaderboard():
    if not os.path.exists("leaderboard.json"):
        return []
    with open("leaderboard.json", "r") as f:
        return json.load(f)

def save_score(name, score, distance):
    data = load_leaderboard()
    exists = next((item for item in data if item["name"] == name), None)
    
    if exists:
        if score > exists["score"]:
            exists["score"] = score
            exists["distance"] = int(distance)
    else:
        data.append({"name": name, "score": score, "distance": int(distance)})
        
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(data, f)
    
def get_username(screen):
    font = pygame.font.SysFont("Verdana", 30)
    name = ""
    while True:
        screen.fill(sprites.BLACK)
        txt = font.render("Enter Name: " + name, True, sprites.WHITE)
        screen.blit(txt, (50, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != "":
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

def show_leaderboard(screen):
    font = pygame.font.SysFont("Verdana", 15)
    data = load_leaderboard()
    while True:
        screen.fill(sprites.BLACK)
        title = font.render("TOP 10 LEADERBOARD (PRESS ANY KEY)", True, sprites.GREEN)
        screen.blit(title, (40, 50))
        for i, entry in enumerate(data):
            msg = f"{i + 1}. {entry['name']} - {entry['score']} pts ({entry['distance']}m)"
            screen.blit(font.render(msg, True, sprites.WHITE), (40, 100 + i * 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                return

def main():
    pygame.init()

    FPS = 60
    FramePerSec = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((sprites.WIDTH, sprites.HEIGHT))
    pygame.display.set_caption("Racer")
    username = get_username(SCREEN)

    font_small = pygame.font.SysFont("Verdana", 20)

    background = pygame.image.load("assets/Road.png")
    background = pygame.transform.scale(background, (400, 600))
    
    distance_driven = 0
    total_score = 0
    
    try:
        crash_sound = pygame.mixer.Sound('assets/accident.mp3')
        coin_sound = pygame.mixer.Sound('assets/coin_taken.wav')
    except pygame.error:
        print('Audiofiles not found')
        crash_sound = coin_sound = None
            
    P1 = sprites.Player()

    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    all_sprites.add(P1)
    
    for _ in range(2):
        new_enemy = sprites.Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        
    SPAWN_POWERUP = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_POWERUP, 10000)
    
    SPAWN_OBSTACLE = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_OBSTACLE, 5000)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 2000)
    
    C1 = sprites.Coin()
    coins.add(C1)
    all_sprites.add(C1)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == INC_SPEED:
                sprites.SPEED += 0.1
                
            if event.type == SPAWN_OBSTACLE:
                obstacle_type = random.choice(['barrier', 'oil'])
                new_obstacle = sprites.Obstacle(obstacle_type)
                if not pygame.sprite.collide_rect(new_obstacle, P1):
                    obstacles.add(new_obstacle)
                    all_sprites.add(new_obstacle)
            
            if event.type == SPAWN_POWERUP:
                if len(power_ups) == 0:
                    new_pu = sprites.PowerUp()
                    power_ups.add(new_pu)
                    all_sprites.add(new_pu)
                
        for entity in all_sprites:
            entity.move()
            distance_driven += sprites.SPEED * 0.1
            total_score = (sprites.SCORE * 100) + int(distance_driven)
            
        if distance_driven >= sprites.GOAL:
            save_score(username, total_score, distance_driven)
            show_leaderboard(SCREEN)
            running = False
            
        pu_hit = pygame.sprite.spritecollideany(P1, power_ups)
        if pu_hit:
            if pu_hit.type == 'nitro':
                P1.nitro_until = current_time + 5000
                P1.slow_until = 0
            elif pu_hit.type == 'shield':
                P1.has_shield = True
            elif pu_hit.type == 'repair':
                for enemy in enemies:
                    if enemy.rect.y > 0:
                        enemy.spawn()
                        break
            pu_hit.kill()
            
        deadly_hit = pygame.sprite.spritecollide(P1, enemies, False)
        hit_obstacles = pygame.sprite.spritecollide(P1, obstacles, False)
        barrier_hit = any(o.type == "barrier" for o in hit_obstacles)
            
        if deadly_hit or barrier_hit:
            if P1.has_shield:
                P1.has_shield = False
                for e in deadly_hit:
                    e.spawn()
            else:
                if crash_sound:
                    crash_sound.play()
                save_score(username, total_score, distance_driven)
                show_leaderboard(SCREEN)
                running = False
        
        oil_hits = any(o.type == 'oil' for o in hit_obstacles)
        if oil_hits:
            P1.slow_until = pygame.time.get_ticks() + 5000
        
        collided_coin = pygame.sprite.spritecollideany(P1, coins)
        if collided_coin:
            sprites.SCORE += 1
            if coin_sound:
                coin_sound.play()
                
            collided_coin.spawn()
            while pygame.sprite.collide_rect(collided_coin, P1):
                collided_coin.spawn()
                
            
        SCREEN.blit(background, (0, 0))
        
        for entity in all_sprites:
            SCREEN.blit(entity.image, entity.rect)
            
        score_label = font_small.render(f"SCORE: {total_score} |{username}", True, sprites.GREEN)
        speed_label = font_small.render(f"FINISH: {int(sprites.GOAL - distance_driven)}", True, sprites.BLACK)
        SCREEN.blit(score_label, (10, 10))
        SCREEN.blit(speed_label, (300, 10))
        
        if current_time < P1.nitro_until:
            timer = (P1.nitro_until - current_time) // 1000
            txt = font_small.render(f"NITRO ACTIVE: {timer}s", True, (0, 255, 255))
            SCREEN.blit(txt, (10, 70))
            
        if P1.has_shield:
            txt = font_small.render("SHIELD READY", True, (255, 255, 0))
            SCREEN.blit(txt, (10, 95))
        
        if pygame.time.get_ticks() < P1.slow_until:
            slow_label = font_small.render("OIL SLICK! SLOWED (5s)", True, (255, 100, 0))
            SCREEN.blit(slow_label, (110, 40))
        
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
    