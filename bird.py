import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, scale = 1):
        super().__init__()# The bird inherits a class Sprite
        self.image = pygame.image.load('images/flappy-bird-image.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.baseImage = self.image # Base image used for rotating the bird sprite during flight as rotationg of a single image causes weird behaviour
        self.rect = self.image.get_rect(center=(200, 300))
        self.gravity = 0

    def update(self, dt):
        self.gravity += 60 * dt #gravity for the bird
        self.image = pygame.transform.rotate(self.baseImage, -self.gravity*.8)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y += self.gravity

    def jump(self):
        self.gravity = -12  #forces the bird to go up

    # Reset the bird's position
    def position_reset(self):
        #self.rect = self.image.get_rect(center=(150, 250))
        self.rect.center = (200, 300)
        self.gravity = 0

    def is_dead(self, floor = 50, celling = -20, colliders = []):
        dead = self.rect.top < celling or self.rect.bottom > pygame.display.get_window_size()[1]-floor
        for c in colliders:
            if self.rect.colliderect(c):
                dead = True
                break
        return dead