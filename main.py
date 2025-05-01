import pygame
from sys import exit
from os.path import exists
from sliding_image import SlidingImage
from bird import Bird
from vodoinstalacija import PVC

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
textFont = pygame.font.Font('pixelated_elegance.ttf', 30) # Font for text
scoreFont = pygame.font.Font('pixelated_elegance.ttf', 90) # Font for the score displayed in the game loop
endScoreFont = pygame.font.Font('pixelated_elegance.ttf', 130) # Font for the score displayed in the game loop

#    | Game state
#  0 : start screen
#  1 : game loop
# -1 : game over screen
gameState = 0

dt = .016 # DeltaTime, used to keep movement and animation time based, instead of frame-rate based as frame rate can vary.

# Speed of scrolling images, pipes and coins
speed = -145

# Scrolling images for the background and floor
background = SlidingImage('images/background_temp.png',(0,-50),0,.75)
floor = SlidingImage('images/floor_temp.png',(0,670),0,.7)
buttonImg = pygame.image.load('images/button_temp.png').convert_alpha()
buttonImg = pygame.transform.scale(buttonImg, (200,80))

# Button
button_rect = pygame.Rect(0, 0, 200, 80)
button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

bird = Bird() # Creating object with Bird class

# Distance between pipes ( from the middle of each pipe )
pipeDis = 400
# Pool the needed amount of pipes in a list
pipework = [PVC((-500,0), 200) for i in range(5)]
# Index of pipe to check for being out of bounds as only the first pipe in the row needs to be checked
# The index will be looped around upon reaching the end of the list
boundsPipe = 0
# Check pipe is the one to be checked for if the bird has passed through it or not
checkPipe = 0

# The current player score
score = 0

# Create a file for storing the high score if one doesn't exist
if not exists('score.txt'):
    with open('score.txt','w') as f: pass

# Read the previous high score from file and store it in a variable
with open('score.txt','r') as f:
    temp = f.read()
    highScore = int(temp) if temp != '' else 0
    del temp

# Simple function to reduce repeating code
# Sets the same speed to all elements ( other than the background )
def set_speeds(speed):
    PVC.speed = speed
    floor.speed = speed
    background.speed = speed/5

highScoreText = scoreText = 0
highScoreRect = scoreRect = 0

buttonText = textFont.render("Start", True, "White")
buttonTextRect = buttonText.get_rect(center=button_rect.center)

while True:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below

        if not gameState: # Starting the game for the first time
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    bird.position_reset()
                    for i in range(len(pipework)):
                        pipework[i].position = (screen.get_width()+i*pipeDis+pipework[i].scale[0],0)
                        pipework[i].randomize()
                    set_speeds(speed)
                    gameState = 1

        elif gameState == 1: # If the game state is active, the code runs
            if event.type == pygame.KEYDOWN: # Jumping method for the bird by clicking either space button or left mouse button
                if event.key == pygame.K_SPACE: # Space button click
                    bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse click
                    bird.jump()

        elif gameState == -1: # if the game state is inactive, restart by clicking the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # If we click with the left mouse click on the button, it resets the game state
                    if button_rect.collidepoint(event.pos): # If reset button is clicked, the game restarts
                        bird.position_reset()
                        gameState = 1
                        set_speeds(speed)
                        for i in range(len(pipework)):
                            pipework[i].position = (screen.get_width()+i*pipeDis+pipework[i].scale[0],0)
                            pipework[i].randomize()
                        score = 0

    # Update position of and draw the scrolling background and floor
    background.update(screen, dt)

    # Update all the pipes
    for pipe in pipework:
        pipe.update(screen, dt if gameState == 1 else 0)

    if gameState == 1: # Executes the code if the game state is game loop
        bird.update(dt) # Executing the code meant for the bird to "fly"
        if bird.rect.top < 0 or bird.rect.bottom > 670 or bird.rect.colliderect(pipework[boundsPipe].topRect) or bird.rect.colliderect(pipework[boundsPipe].bottomRect):
            gameState = -1
            boundsPipe = 0
            checkPipe = 0
            set_speeds(0)

            if highScore < score:
                highScore = score
                with open('score.txt','w') as f:
                    print(highScore, file=f)
            
            # Setting up the text for both the restart button and the text showing the current score and new high score info
            buttonText = textFont.render("Restart", True, "White")
            scoreText = endScoreFont.render('Score: '+str(score), True, "White")
            highScoreText = textFont.render('New High Score!' if highScore == score else 'Previous High Score: '+str(highScore), True, 'Yellow' if highScore == score else  "White")

            # Setting up rects for the text above
            buttonTextRect = buttonText.get_rect(center = button_rect.center)
            scoreRect = scoreText.get_rect(midtop = (screen.get_width()*.5, 70))
            highScoreRect = highScoreText.get_rect(midtop = (screen.get_width()*.5, scoreRect.bottom + 20))
        else:
            if bird.rect.center[0] > pipework[checkPipe].position[0]:
                checkPipe += 1
                if checkPipe == len(pipework):
                    checkPipe = 0
                score += 1
            scoreText = scoreFont.render(str(score), True, "White")
            screen.blit(scoreText, scoreText.get_rect(midtop=(screen.get_width()*.5,30))) # Renders the current score to the top of the screen
            # Check if the first pipe from left to right is out of bounds
            # Moves it to the end of the row if that is the case ( also randomizes the moved pipe )
            # Also increments the checkPipe index and loops it around if needed
            p = pipework[boundsPipe]
            if p.position[0] + p.scale[0] < 0:
                p.position = (pipework[boundsPipe-1 if boundsPipe > 0 else len(pipework)-1].position[0]+pipeDis, p.position[1])
                p.randomize()
                boundsPipe += 1
                if boundsPipe == len(pipework):
                    boundsPipe = 0
    elif not gameState: # Puts the start button on the screen, if the game is in the start screen state
        screen.blit(buttonImg, button_rect)
        screen.blit(buttonText, buttonTextRect)
    elif gameState == -1: # Puts the restart button and the score info text on the screen, if the game is in the game over screen state
        screen.blit(scoreText, scoreRect)
        screen.blit(highScoreText, highScoreRect)
        screen.blit(buttonImg, button_rect)
        screen.blit(buttonText, buttonText.get_rect(center=button_rect.center))

    screen.blit(bird.image, bird.rect)
    floor.update(screen, dt)

    # Renders everything
    pygame.display.flip()

    dt = float(clock.tick(60))/1000.0  # Limits FPS to 60 and assigns a 0 to 1 value to dt ( converts tick value from ms to seconds )