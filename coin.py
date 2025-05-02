import pygame
from random import randint

class Coin(pygame.sprite.Sprite):
    def __init__(self, scale = 1, animFrameRate = 6, position = (0,0), speed = 0):
        super().__init__()
        # Speed of x axis movement
        self.speed = speed
        # Length of time on frame lasts on screen in seconds
        self._frameLength = 1/animFrameRate
        # Local time used for finding the index of the image to be displayed
        self._time = 0
        # List of images to be cycled through for the animation
        self.images = [pygame.transform.rotozoom(pygame.image.load('images/coin/coin_'+str(i)+'.png').convert_alpha(), 0, scale) for i in range(1,7)]
        # Get the rect from the first image and 
        self.rect = self.images[0].get_rect(center=position)
        self.position = position

    def update(self, surf, dt):
        # Increment local time by the elapsed time in last frame
        self._time += dt
        # Calculating the index of the frame to be displayed
        # Mod(Elapsed Time, Total Anim Time) gives us the "local" time in the current animatin cycle
        # Dividing that time by the length of a frame in seconds and converting that result to an int gives us the final index 
        imgIndex = int((self._time % (self._frameLength * len(self.images))) / self._frameLength)
        # Move the coin on the x axis by the given speed
        self.position = (self.position[0] + self.speed * dt, self.position[1])
        self.rect.center = self.position
        # Draw the coin to the screen
        surf.blit(self.images[imgIndex], self.rect)

    # Sets the center position of the rect
    def SetPosition(self, position, randomizeY = False):
        self.position = (position[0], randint(int(self.rect.height*.5),int(pygame.display.get_window_size()[1]-self.rect.height*.5))) if randomizeY \
        else position 
