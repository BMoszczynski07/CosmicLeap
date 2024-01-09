import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400)) # width, height
alien_logo = pygame.image.load("graphics/alien.png")
pygame.display.set_caption("CosmicLeap")
pygame.display.set_icon(alien_logo)
clock = pygame.time.Clock()

running = True

sky_surface = pygame.image.load("graphics/Sky.png")

ground_surface = pygame.image.load("graphics/ground.png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))

    pygame.display.update()
    clock.tick(60) # 60 -> max fps