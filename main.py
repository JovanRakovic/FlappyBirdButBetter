import pygame
from sys import exit

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below 

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightblue")


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60