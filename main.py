import pygame
from sys import exit
import math

pygame.init()

# graphics for window
alien_logo = pygame.image.load("graphics/alien.png")

# init window
screen = pygame.display.set_mode((800, 400)) # width, height
pygame.display.set_caption("CosmicLeap")
pygame.display.set_icon(alien_logo)

# init clock (for FPS)
clock = pygame.time.Clock()

# fonts
main_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 50)
sub_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 32)

# variables
snail_x_pos = 600
player_gravity = .04
running = True
score = 0
start_time = 0
game_active = False

# surfaces
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
title_surface = main_font.render("Welcome to CosmicLeap!", False, (0,0,0))
title_rect = title_surface.get_rect(topleft = (screen.get_width() / 2 - title_surface.get_width() / 2, 25))
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (snail_x_pos, 300))
player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,250))

def handleGetTime(elapsed_time):
    hours = math.floor(elapsed_time / 3600 / 1000)
    minutes = f"0{math.floor(elapsed_time / 60 / 1000) % 60}" if math.floor(elapsed_time / 60 / 1000) % 60 < 10 else math.floor(elapsed_time / 60 / 1000) % 60
    seconds = f"0{math.floor(elapsed_time / 1000) % 60}" if math.floor(elapsed_time / 1000) % 60 < 10 else math.floor(elapsed_time / 1000) % 60

    return f"{hours}:{minutes}:{seconds}"

def displayTime():
    current_time = pygame.time.get_ticks() - start_time

    SCORE_CONSTANT = 73.5

    global score
    score = int(pygame.time.get_ticks() / SCORE_CONSTANT)

    timer_text = sub_font.render(f"Time: {handleGetTime(current_time)}", False, (0,0,0))
    timer_rect = timer_text.get_rect(topleft=(10, 50))
    screen.blit(timer_text, timer_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.collidepoint(80, 216):
                    player_gravity = -3
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = screen.get_width()
                start_time = pygame.time.get_ticks()


        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("collision")

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        screen.blit(title_surface, title_rect)
        screen.blit(snail_surface, snail_rect)

        displayTime()

        # score
        score_text = sub_font.render(f"Score: {score}", False, (0, 0, 0))
        score_rect = score_text.get_rect(topleft=(10, 30))
        screen.blit(score_text, score_rect)

        # Player
        # print(player_rect.y)

        player_gravity += .04

        if player_rect.y + player_gravity > 214:
            player_rect.y = 216

        if player_rect.y + player_gravity < 216:
            player_rect.y += player_gravity

        screen.blit(player_surface, player_rect)

        # Snail
        snail_rect.x -= 2

        if snail_rect.x < -100:
            snail_rect.x = screen.get_width()
    else:
        screen.fill((100,100,100))

    # collision
    if snail_rect.colliderect(player_rect):
        game_active = False

    # if player_rect.colliderect(snail_rect): # returns 0 or 1 (also we dont need to write == 0 or == 1)

    # mouse_pos = pygame.mouse.get_pos()

    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    clock.tick(300) # max fps

    fps = clock.get_fps()

    fps_text = sub_font.render(f"FPS: {int(fps)}", False, (0,0,0))
    screen.blit(fps_text, (10, 10))

    pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_SPACE]:
    #     print("jump!")

    # pygame.draw.line(screen, "Gold", (0,0), pygame.mouse.get_pos(), 10)

    # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100)) # left, top, width, height


    pygame.display.flip()