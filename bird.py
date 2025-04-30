import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()# The bird inherits a class Sprite
        self.image = pygame.image.load('images/flappy-bird-image.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .15)
        self.rect = self.image.get_rect(center=(200, 300))
        self.gravity = 0

    def update(self, dt):
        self.gravity += 60 * dt #gravity for the bird
        self.rect.y += self.gravity

    def jump(self):
        self.gravity = -12  #forces the bird to go up

    # Reset the bird's position
    def position_reset(self):
        #self.rect = self.image.get_rect(center=(150, 250))
        self.rect.center = (200, 300)
        self.gravity = 0