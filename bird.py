import pygame
from sfx import SFX
pygame.init()

sfx = SFX()

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
        sfx.birdflap_sfx.play()

    # Reset the bird's position
    def position_reset(self):
        #self.rect = self.image.get_rect(center=(150, 250))
        self.rect.center = (200, 300)
        self.gravity = 0

    # Collision detection with the earth, heaven and a provided list of rects
    def is_dead(self, floor = 50, celling = -20, colliders = []):
        # Check for the floor and sky
        dead = self.rect.top < celling or self.rect.bottom > pygame.display.get_window_size()[1]-floor
        # Custom implementation for circular collision detection as none was provided by pygame
        for c in colliders:
            # Abs distance from the center of the bird to the center of the rectangle, allows calculations as if only one corner exists
            circleDistance = (abs(self.rect.center[0] - c.center[0]), abs(self.rect.center[1] - c.center[1]))
            # Sotring frequently used values as to avoid repeated calculation
            rectHalf = (c.width/2, c.height/2)
            birbRadius = self.rect.height/2

            # Check if the bird is outside the possible collision radius
            if (circleDistance[0] > (rectHalf[0] + birbRadius) or circleDistance[1] > (rectHalf[1] + birbRadius)): 
                continue

            # Check if the bird is coliding with one of the sides
            if (circleDistance[0] <= rectHalf[0] or circleDistance[1] <= rectHalf[1]):
                dead = True
                break

            # Check if the bird is colliding with the corner
            cornerDistance_sq = (circleDistance[0]- rectHalf[0])**2 + (circleDistance[1] - rectHalf[1])**2
            dead = (cornerDistance_sq <= birbRadius**2)
        return dead