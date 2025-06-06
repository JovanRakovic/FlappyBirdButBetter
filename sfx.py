import pygame
from random import choice

#Class for storing and playing music and sounds
class SFX:
    def __init__(self):
        pygame.mixer.init()
        self.button = pygame.mixer.Sound("./sfx/button.mp3")
        self.coin_collect = pygame.mixer.Sound("./sfx/coin.wav")
        self.pipe_pass = pygame.mixer.Sound("./sfx/pipe_pass.wav")
        self.birdflap_sfx = pygame.mixer.Sound("./sfx/woosh.mp3")
        self.bg_music = ["./sfx/song1.mp3", "./sfx/song2.mp3", "./sfx/song3.mp3"]
        self.bwawk =   [pygame.mixer.Sound("./sfx/death_1.mp3"),
                        pygame.mixer.Sound("./sfx/death_2.mp3"),
                        pygame.mixer.Sound("./sfx/death_3.mp3"),
                        pygame.mixer.Sound("./sfx/death_4.mp3")]

    def play_button(self, volume=0.5):
        self.button.set_volume(volume)
        self.button.play()

    def play_random_music(self, volume=0.4):
        music = choice(self.bg_music)
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def play_pipe_pass(self, volume = 0.3):
        self.pipe_pass.set_volume(volume)
        self.pipe_pass.play()

    def play_random_death(self):
        sound = choice(self.bwawk)
        sound.play()

    def play_coin_collect(self, volume = 0.5):
        self.coin_collect.set_volume(volume)
        self.coin_collect.play()