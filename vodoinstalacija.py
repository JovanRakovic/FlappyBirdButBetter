import pygame
from math import sin, pi
from random import randint, random

# Class for flappy bird pipes

class PVC:
    speed = 0

    def __init__(self, position, gap, amplitude=0, frequency=1, scale = (100,600)):
        self.position = position
        self.halfGap = int(gap/2)
        self.amp = amplitude
        self.freq = frequency
        self._time = random() # _time is used for animating the moving pipes
        self.scale = scale

        # Setup top and bottom pipe images
        self.bottomImg = pygame.image.load('images/pipe_temp.png').convert_alpha()
        self.bottomImg = pygame.transform.scale(self.bottomImg, scale)
        self.topImg = pygame.transform.flip(self.bottomImg, False, True)

        # Get rects for collision and positioning of top and bottom pipes
        self.bottomRect = self.bottomImg.get_rect()
        self.topRect = self.topImg.get_rect()

    # Move and draw the pipes
    def update(self, surf, dt):
        self.position = (self.position[0] + PVC.speed * dt, self.position[1]) # Change the x position by the given speed
        self._time += dt # Increment time by the delta time period
        self._update_rects() # Update rect positions
        surf.blit(self.topImg, self.topRect)
        surf.blit(self.bottomImg, self.bottomRect)
    
    # Randomize the pipe's y location and decide whether it is moving or not
    def randomize(self):
        self._time = random()
        if randint(0,101) > 80: # 10%c chance of a pipe being a moving one ( might make an adaptive threshold in the future ) 
            self.amp = 100
            self.freq = .7
        else:
            self.amp = 0
        self.position = (self.position[0], randint(self.halfGap, pygame.display.get_window_size()[1] - 60 - self.halfGap))
        # Random y position between the top and bottom of the screen accounting for the size of the gap and the floor

    # Update the position of the rects
    def _update_rects(self):
        # offset is used for animating the pipes without ever changing the base position
        # Ternary operator used to avoid the sin function and the equation within when amplitude is 0
        # (sin()+1) *.5 shifts the sin return value from -1:1 to 0:1
        offset = self.amp * (sin(self._time*2*pi*self.freq)+1)*.5 if self.amp > 0 else 0
        # Set the pipe positions based on the gap height and the offset
        self.bottomRect.midtop = (self.position[0], self.position[1]+self.halfGap+offset)
        self.topRect.midbottom = (self.position[0], self.position[1]-self.halfGap-offset)