import pygame
from sys import exit

pygame.init()

# graphics for window
alien_logo = pygame.image.load("graphics/alien.png")

# init window
screen = pygame.display.set_mode((800, 400)) # width, height
pygame.display.set_caption("CosmicLeap")
pygame.display.set_icon(alien_logo)

# init clock (FPS)
clock = pygame.time.Clock()

# fonts
main_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 50)
sub_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 32)

running = True

# variables
snail_x_pos = 600

# surfaces
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
title_surface = main_font.render("Welcome to CosmicLeap!", False, (0,0,0))
title_rect = title_surface.get_rect(topleft = (screen.get_width() / 2 - title_surface.get_width() / 2, 25))
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (snail_x_pos, 300))
player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

player_gravity = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -3

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -3

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("collision")

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(title_surface, title_rect)
    screen.blit(snail_surface, snail_rect)

    # Player
    print(player_rect.y)

    player_gravity += .04

    if player_rect.y + player_gravity < 216:
        player_rect.y += player_gravity

    screen.blit(player_surface, player_rect)

    if snail_rect.left < -100:
        snail_rect.left = screen.get_width()
    else:
        snail_rect.left -= 2

    # if player_rect.colliderect(snail_rect): # returns 0 or 1 (also we dont need to write == 0 or == 1)

    # mouse_pos = pygame.mouse.get_pos()

    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    clock.tick(300) # max fps

    fps = clock.get_fps()

    fps_text = sub_font.render(f"FPS: {int(fps)}", False, (0,0,0))
    screen.blit(fps_text, (10, 10))

    score_text = sub_font.render(f"Score: 0", False, (0,0,0))
    score_rect = score_text.get_rect(topleft = (10, 30))

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_SPACE]:
    #     print("jump!")

    # pygame.draw.line(screen, "Gold", (0,0), pygame.mouse.get_pos(), 10)

    # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100)) # left, top, width, height

    screen.blit(score_text, score_rect)

    pygame.display.flip()