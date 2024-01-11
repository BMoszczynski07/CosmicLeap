import pygame
from sys import exit
import math
from random import randint
from Player import Player
from Obstacle import Obstacle

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

# variables (for main page)
snail_x_pos = 600
player_gravity = .04
running = True
score = 0
start_time = 0
speed = 0
game_active = False

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# variables (for welcome page)

# surfaces (for welcome page)
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (190,225))
player_stand_rect = player_stand.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

welcome_text = main_font.render("Welcome to CosmicLeap", False, (182, 219, 61))
start_text = sub_font.render("> Press SPACE to start the game <", False, (182, 219, 61))

welcome_text_rect = welcome_text.get_rect(center = (screen.get_width() / 2, 40))
start_text_rect = welcome_text.get_rect(center = (screen.get_width() / 2, screen.get_height() - 30))

# surfaces (for main page)
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
title_surface = main_font.render("CosmicLeap", False, (0,0,0))
title_rect = title_surface.get_rect(topleft = (screen.get_width() / 2 - title_surface.get_width() / 2, 25))

# obstacles' surfaces
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_id = 0

snail_surf = snail_frames[snail_frame_id]

fly_frame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_id = 0

fly_surf = fly_frames[fly_frame_id]

# player's surfaces
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_index = 0

player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom = (80,250))

obstacle_rect_list = []

def player_animation():
    # play walking animation if the player is on floor
    # display the jump surface when player is not on floor
    global player_surface, player_index

    if player_rect.bottom < 300:
        # jump
        player_surface = player_jump
    else:
        player_index += 0.025
        if player_index >= len(player_walk):
            player_index = 0

        player_surface = player_walk[int(player_index)]
        # walk

def handleGetTime(elapsed_time):
    hours = math.floor(elapsed_time / 3600 / 1000)
    minutes = f"0{math.floor(elapsed_time / 60 / 1000) % 60}" if math.floor(elapsed_time / 60 / 1000) % 60 < 10 else math.floor(elapsed_time / 60 / 1000) % 60
    seconds = f"0{math.floor(elapsed_time / 1000) % 60}" if math.floor(elapsed_time / 1000) % 60 < 10 else math.floor(elapsed_time / 1000) % 60

    return f"{hours}:{minutes}:{seconds}"

def displayTime():
    current_time = pygame.time.get_ticks() - start_time

    SCORE_CONSTANT = 73.5

    global score
    score = int((pygame.time.get_ticks() - start_time) / SCORE_CONSTANT)

    timer_text = sub_font.render(f"Time: {handleGetTime(current_time)}", False, (0,0,0))
    timer_rect = timer_text.get_rect(topleft=(10, 50))
    screen.blit(timer_text, timer_rect)

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

def obstacle_movement(obstacle_list):
    updated_obstacle_list = []
    if obstacle_list:
        for obstacle_rect in obstacle_list:

            obstacle_rect.left -= 2 + speed

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

            updated_obstacle_list.append(obstacle_rect)

    updated_obstacle_list = [obstacle for obstacle in updated_obstacle_list if obstacle.left > -100]
    return updated_obstacle_list

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.rect.bottom = 300
        return False
    return True

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
                obstacle_rect_list = []
                game_active = True
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle("fly" if randint(0,2) else "snail"))
            # if randint(0,2):
            #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
            # else:
            #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))
            print(obstacle_rect_list)

        if event.type == snail_animation_timer and game_active:
            if snail_frame_id == 0: snail_frame_id = 1
            else: snail_frame_id = 0

            snail_surf = snail_frames[snail_frame_id]

        if event.type == fly_animation_timer and game_active:
            if fly_frame_id == 0: fly_frame_id = 1
            else: fly_frame_id = 0

            fly_surf = fly_frames[fly_frame_id]


        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("collision")

    clock.tick(300)  # max fps
    fps = clock.get_fps()

    if game_active:
        speed += 0.0001

        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        screen.blit(title_surface, title_rect)


        fps_text = sub_font.render(f"FPS: {int(fps)}", False, (0, 0, 0))
        screen.blit(fps_text, (10, 10))

        pygame.time.get_ticks()

        # score
        score_text = sub_font.render(f"Score: {score}", False, (0, 0, 0))
        score_rect = score_text.get_rect(topleft=(10, 30))
        screen.blit(score_text, score_rect)

        displayTime()

        # Player
        # print(player_rect.y)

        # player_gravity += .04

        # if player_rect.y + player_gravity > 214:
        #     player_rect.y = 216
        #
        # if player_rect.y + player_gravity < 216:
        #     player_rect.y += player_gravity

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # player_animation()
        # screen.blit(player_surface, player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

        # collision
        # game_active = collisions(player_rect, obstacle_rect_list)

        # Snail
        # snail_rect.x -= 2

        # if snail_rect.x < -100:
        #     snail_rect.x = screen.get_width()
    else:
        speed = 0

        screen.fill((100,100,100))

        fps_text = sub_font.render(f"FPS: {int(fps)}", False, (182,219,61))
        screen.blit(fps_text, (10, 10))

        player_rect.midbottom = (80,300)
        player_gravity = 0

        screen.blit(player_stand, player_stand_rect)
        screen.blit(welcome_text, welcome_text_rect)

        if score == 0: screen.blit(start_text, start_text_rect)
        else:
            sub_score_text = sub_font.render(f"Your score: {score}", False, (182, 219, 61))
            sub_score_text_rect = sub_score_text.get_rect(center=(screen.get_width() / 2, screen.get_height() - 30))
            screen.blit(sub_score_text, sub_score_text_rect)

    # if player_rect.colliderect(snail_rect): # returns 0 or 1 (also we dont need to write == 0 or == 1)

    # mouse_pos = pygame.mouse.get_pos()

    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_SPACE]:
    #     print("jump!")

    # pygame.draw.line(screen, "Gold", (0,0), pygame.mouse.get_pos(), 10)

    # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100)) # left, top, width, height


    pygame.display.flip()