import pygame.sprite
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_frame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        elif type == "snail":
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.speed = 0

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.025

        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def move_to_left(self):
        self.speed += 0.0001

        self.rect.left -= 2 + self.speed

    def destroy(self):
        if self.rect.left <= -100:
            self.kill() # destroying obstacle

    def update(self):
        self.animation_state()
        self.move_to_left()
        self.destroy()