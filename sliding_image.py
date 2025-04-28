import pygame

# Class for repeateing sliding images

class SlidingImage:
    def __init__(self, imagePath, position, speed=0, scale=1):
        self._speed = speed
        self._position = position
        self.image = pygame.image.load(imagePath).convert()
        self.image = pygame.transform.rotozoom(self.image, 0, scale) # rotzoom function prefered to scale due to filtering
        self._width = self.image.get_width() # Storing the width so the get_width function doesn't need to be called repeatedly
        self._offset = 0
        self._calculate_repeats()

    # Update the image offset and draw the duplciated + offset images to the screen
    def update(self, surf, dt):
        for i in range(0,self._repeatsRight):
            surf.blit(self.image, (self._position[0]+i*self._width+self._offset, self._position[1]))
        for i in range(1,self._repeatsLeft): # we can skip the 0 index as it has been drawn in the loop above
            surf.blit(self.image, (self._position[0]-i*self._width+self._offset, self._position[1]))
        # update the offset
        self._offset += self._speed * dt
        if(abs(self._offset) >= self._width): # Loop the offset back around if it exceeds the width of the image
            self._offset = self._width%self._offset

    # The amount of times the image needs to be drawn to make the sliding seamless
    # Repeat values calculated for both sides of the image for efficiency
    def _calculate_repeats(self):
        self._repeatsRight = (pygame.display.get_window_size()[0] - self._position[0])//self._width + 2
        self._repeatsLeft =  self._position[0]//self._width + 2
        # available width // image width + 1 is enough for a stationary image to be displayed
        # but a moving one requires an additional image in the row to not break the seamlessnes 

    def set_speed(self, speed):
        self._speed = speed