import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()# The bird inherits a class Sprite
        self.image = pygame.image.load('images/flappy-bird-image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(200, 250))
        self.gravity = 0

    def update(self):
        self.gravity += 1 #gravity for the bird
        self.rect.y += self.gravity

    def jump(self):
        self.gravity = -15  #forces the bird to go down

    def is_dead(self):
        return self.rect.top <= 0 or self.rect.bottom >= 500 #game over state when fall or go above the screen