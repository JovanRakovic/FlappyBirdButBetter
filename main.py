import pygame
from sys import exit
from sliding_image import SlidingImage
from bird import Bird

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 60) #will be added in the meantime

dt = .016 # DeltaTime, used to keep movement and animation time based, instead of frame-rate based as frame rate can vary.

speed = -145

background = SlidingImage('images/background_temp.png',(0,-50),speed/5,.75)
floor = SlidingImage('images/floor_temp.png',(0,670),speed,.7)

# Button
button_rect = pygame.Rect(0, 0, 200, 80)
button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

bird = Bird() #Creating object with Bird class

#Initializing the game states before loop
game_active = False
game_started = False

while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below

        if not game_started:  # Starting the game for the first time
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    bird.position_reset()
                    game_started = True
                    game_active = True

        elif game_active: #If the game state is active, the code runs
            if event.type == pygame.KEYDOWN:  #Jumping method for the bird by clicking either space button or left mouse button
                if event.key == pygame.K_SPACE:  #Space button click
                    bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #Left mouse click
                    bird.jump()

        elif not game_active: #if the game state is inactive, restart by clicking the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # If we click with the left mouse click on the button, it resets the game state
                    if button_rect.collidepoint(event.pos): #If reset button is clicked, the game restarts
                        bird.position_reset()
                        game_active = True

    background.update(screen, dt)
    floor.update(screen, dt)

    if game_active and game_started: #Executes the code if the game state is "active" and "started"
        bird.update() #Executing the code meant for the bird to "fly"
        screen.blit(bird.image, bird.rect)
        if bird.is_dead(): #Checks if the bird state is alive, if it's not, puts the game in no active state
            game_active = False
    elif not game_started: # Puts the start button on the screen, if the game is in inactive but started state
        button_text = font.render("Start", True, "White")
        pygame.draw.rect(screen, "gray", button_rect, border_radius=12)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))
    elif game_started and not game_active: #Puts the restart button on the screen, if the game is in inactive state
        button_text = font.render("Restart", True, "White")
        pygame.draw.rect(screen, "gray", button_rect, border_radius=12)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = float(clock.tick(60))/1000.0  # limits FPS to 60 and assigns a 0 to 1 value to dt ( converts tick value from ms to seconds )