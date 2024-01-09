import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400)) # width, height
pygame.display.set_caption("CosmicLeap")
# pygame.display.set_icon()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw all our elements
    # update everything
    pygame.display.update()