import pygame
from sys import exit
from sliding_image import SlidingImage
from bird import Bird

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

dt = .016 # DeltaTime, used to keep movement and animation time based, instead of frame-rate based as frame rate can vary.

speed = -145

background = SlidingImage('images/background_temp.png',(0,-50),speed/5,.75)
floor = SlidingImage('images/floor_temp.png',(0,670),speed,.7)
bird = Bird()
while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below
        if event.type == pygame.KEYDOWN:  #Jumping method for the bird by clicking either space button or left mouse button
            if event.key == pygame.K_SPACE:  #Space button click
                bird.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #Left mouse click
                bird.jump()
    background.update(screen, dt)
    floor.update(screen, dt)

    bird.update() #Executing the code meant for the bird to "fly"
    screen.blit(bird.image, bird.rect) #

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = float(clock.tick(60))/1000.0  # limits FPS to 60 and assigns a 0 to 1 value to dt ( converts tick vlaue from ms to seconds )