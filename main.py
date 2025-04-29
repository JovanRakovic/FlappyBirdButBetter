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

# Reset button
font = pygame.font.Font(None, 60) #will be added in the meantime
button_text = font.render("Restart", True, "White")
button_rect = pygame.Rect(0, 0, 200, 80)
button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

bird = Bird() #Creating object with Bird class
game_active = True #Setting the game state to active

while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below

        if game_active: #Checking if the game state is active
            if event.type == pygame.KEYDOWN:  #Jumping method for the bird by clicking either space button or left mouse button
                if event.key == pygame.K_SPACE:  #Space button click
                    bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #Left mouse click
                    bird.jump()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # If we click with the left mouse click on the button, it resets the game state
                    if button_rect.collidepoint(event.pos): #If reset button is clicked, the game restarts
                        bird.position_reset()
                        game_active = True

    if game_active: #Executes the code if the game state is active
        background.update(screen, dt)
        floor.update(screen, dt)
        bird.update() #Executing the code meant for the bird to "fly"
        screen.blit(bird.image, bird.rect)
        if bird.is_dead(): #Checks if the bird state is alive, if it's not, puts the game in no active state
            game_active = False
    else:
        # Puts the reset button if the game is in no active state
        pygame.draw.rect(screen, "gray", button_rect, border_radius=12)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = float(clock.tick(60))/1000.0  # limits FPS to 60 and assigns a 0 to 1 value to dt ( converts tick value from ms to seconds )