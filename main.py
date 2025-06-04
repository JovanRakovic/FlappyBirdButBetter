import pygame
import random
from sys import exit
from os.path import exists
from sliding_image import SlidingImage
from bird import Bird
from vodoinstalacija import PVC
from coin import Coin
from sfx import SFX
from random import randint


# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
textFont = pygame.font.Font('pixelated_elegance.ttf', 30) # Font for text
scoreFont = pygame.font.Font('pixelated_elegance.ttf', 90) # Font for the score displayed in the game loop
endScoreFont = pygame.font.Font('pixelated_elegance.ttf', 130) # Font for the score displayed in the game loop
inputFont = pygame.font.Font('pixelated_elegance.ttf', 25) #Font for the input box

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

# Button rect size and positioning
button_rect = pygame.Rect(0, 0, 200, 80)
button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

bird = Bird(.132) # Creating object with Bird class

sfx = SFX() # Object with SFX class

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
highScore = 0

# Create a file for storing the leaderboard if one doesn't exist
if not exists('leaderboard.txt'):
    with open('leaderboard.txt', 'w') as f: pass

# Read the leaderboard and store the players in a list
with open('leaderboard.txt', 'r') as l:
    temp = l.read()
    leaderboard = temp.split(", ") if temp != '' else []
    del temp

# Variables to be later used for rendering score and high score to the screen upon the end of the game loop
highScoreText = scoreText = 0
highScoreRect = scoreRect = 0

# Variables for the start/restart button text
playerName = ''
inputBoxActive = False 
# buttonText chnages its content based on the game state
buttonText = textFont.render("Start", True, "White")
buttonTextRect = buttonText.get_rect(center=button_rect.center)
leaderboardText = textFont.render('leaderboard: ' if leaderboard else '', True, 'Yellow')
leaderboardRect = leaderboardText.get_rect(midtop = (screen.get_width()*.5, 50))
inputBox = pygame.Rect(screen.get_width()*.5 - 150, 600, 300, 40)


# Single coin that will be reused and moved every time it either reaches the end of the screen or is touched by the bird
coin = Coin(.75,10,(-500,0))

# Simple function to reduce repeating code
# Sets the same speed to all elements ( other than the background )
def set_speeds(speed):
    PVC.speed = speed
    floor.speed = speed
    background.speed = speed/5
    coin.speed = speed

# Function for setting the peramiters needed to start the game loop
def enter_game_loop():
    bird.position_reset()
    sfx.play_button()
    sfx.play_random_music()
    for i in range(len(pipework)):
        pipework[i].position = (screen.get_width()+i*pipeDis+pipework[i].scale[0],0)
        pipework[i].randomize()
    coin.SetPosition((pipeDis * (randint(5,10) + .5) + pipework[checkPipe].position[0], 0), True)
    set_speeds(speed)


while True:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Saves and sorts the leaderboard right before uninitializing pygame
            if highScore>0:
                leaderboard.append(f"{playerName}: {highScore}")
                leaderboard = sorted(leaderboard, key=lambda x: int(x.rsplit(' ', 1)[-1]), reverse=True)
                with open('leaderboard.txt', 'w') as l:
                    print(', '.join(leaderboard), file=l)
            pygame.quit() # Uninitilizes pygame
            exit()        # Exits the application without executing the code below

        if not gameState: # Starting the game for the first time
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    if playerName: #Player name is needed before starting game
                        enter_game_loop()
                        gameState = 1
                        inputBoxActive = False
                elif inputBox.collidepoint(event.pos): #Inputting your name
                    inputBoxActive = True
            if event.type == pygame.KEYDOWN and inputBoxActive:
                if event.key == pygame.K_RETURN:
                    inputBoxActive = False
                elif event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                elif len(playerName) < 6:
                    playerName += event.unicode
            pygame.draw.rect(screen, "Yellow", inputBox, 2)
            nameText = textFont.render(playerName or "Enter your name", True, "Yellow")
            
                    

        elif gameState == 1: # If the game state is active, the code runs
            if event.type == pygame.KEYDOWN: # Jumping method for the bird by clicking either space button or left mouse button
                if event.key == pygame.K_SPACE: # Space button click
                    bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse click
                    bird.jump()

        else: # if the game state is inactive, restart by clicking the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # If we click with the left mouse click on the button, it resets the game state
                    if button_rect.collidepoint(event.pos): # If reset button is clicked, the game restarts
                        enter_game_loop()
                        score = 0
                        gameState = 1

    # Update position of and draw the scrolling background and floor
    background.update(screen, dt)

    # Update all the pipes
    for pipe in pipework:
        pipe.update(screen, dt if gameState == 1 else 0) # Send 0 instead of dt when not in game loop so the pipes won't move in start/restart screen

    if gameState == 1: # Executes the code if the game state is game loop
        bird.update(dt) # Executing the code meant for the bird to "fly"
        if bird.is_dead(colliders=[pipework[checkPipe].topRect, pipework[checkPipe].bottomRect]):
            sfx.play_random_death()
            gameState = -1
            boundsPipe = 0
            checkPipe = 0
            set_speeds(0)

            if highScore < score:
                highScore = score
            
            # Setting up the text for both the restart button and the text showing the current score and new high score info
            buttonText = textFont.render("Restart", True, "White")
            scoreText = endScoreFont.render('Score: '+str(score), True, "White")
            highScoreText = textFont.render('New High Score!' if highScore == score else 'Previous High Score: '+str(highScore), True, 'Yellow' if highScore == score else  "White")

            # Setting up rects for the text above
            buttonTextRect = buttonText.get_rect(center = button_rect.center)
            scoreRect = scoreText.get_rect(midtop = (screen.get_width()*.5, 70))
            highScoreRect = highScoreText.get_rect(midtop = (screen.get_width()*.5, scoreRect.bottom + 20))
        else:
            if bird.rect.left > pipework[checkPipe].bottomRect.right:
                checkPipe += 1
                if checkPipe == len(pipework):
                    checkPipe = 0
                score += 1
                sfx.play_pipe_pass()

            if bird.rect.colliderect(coin.rect):
                coin.SetPosition((pipeDis * (randint(5,15) + .5) + pipework[checkPipe].position[0], 0), True)
                score += 10
                sfx.play_coin_collect()
            elif coin.rect.right < 0:
                coin.SetPosition((pipeDis * (randint(5,15) + .5) + pipework[checkPipe].position[0], 0), True)

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
        screen.blit(leaderboardText, leaderboardRect)
        screen.blit(nameText, (inputBox.x + 5, inputBox.y + 5))
        line_spacing = 35
        textpos = 100
        for player in leaderboard[:5]:
            playerText = textFont.render(player, True, "Yellow")
            playerRect = playerText.get_rect(midtop = (screen.get_width()*.5, textpos))
            screen.blit(playerText, playerRect)
            textpos += line_spacing
    else: # Puts the restart button and the score info text on the screen, if the game is in the game over screen state
        screen.blit(scoreText, scoreRect)
        screen.blit(highScoreText, highScoreRect)
        screen.blit(buttonImg, button_rect)
        screen.blit(buttonText, buttonText.get_rect(center=button_rect.center))

    coin.update(screen, dt)
    screen.blit(bird.image, bird.rect)
    floor.update(screen, dt)

    # Renders everything
    pygame.display.flip()

    dt = float(clock.tick(60))/1000.0  # Limits FPS to 60 and assigns a 0 to 1 value to dt ( converts tick value from ms to seconds )