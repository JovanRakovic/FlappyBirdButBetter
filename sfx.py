import pygame
from pygame import mixer
from random import choice
pygame.init()

class SFX():
    death_one = pygame.mixer.Sound("./sfx/death_1.mp3")
    death_two = pygame.mixer.Sound("./sfx/death_2.mp3")
    death_three = pygame.mixer.Sound("./sfx/death_3.mp3")
    death_four = pygame.mixer.Sound("./sfx/death_4.mp3")
    button = pygame.mixer.Sound("./sfx/button.mp3")
    coin_collect = pygame.mixer.Sound("./sfx/coin.wav")
    pipe_pass = pygame.mixer.Sound("./sfx/pipe_pass.wav")
    birdflap_sfx = pygame.mixer.Sound("./sfx/woosh.mp3")
    bg_music = ["./sfx/song1.mp3", "./sfx/song2.mp3", "./sfx/song3.mp3"]
    bwawk = [death_one, death_two, death_three, death_four]
    

