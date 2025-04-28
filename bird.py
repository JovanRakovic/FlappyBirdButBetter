import pygame
from sys import exit

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/flappy-bird-image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(150, 250))
        self.gravity = 0

    def update(self):
        self.gravity += 1 #gravity for the bird
        self.rect.y += self.gravity

    def jump(self):
        self.gravity = -15  #forces the bird to go down

    def is_dead(self):
        return self.rect.top <= 0 or self.rect.bottom >= 500 #game over state when fall or go above the screen

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption('Flappy Bird')
bird = Bird()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #or bird.rect.bottom >= 500
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:  #jumping
            if event.key == pygame.K_SPACE:  #space button click
                bird.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #left mouse click
                bird.jump()

    screen.fill("lightblue")

    bird.update()
    screen.blit(bird.image, bird.rect)

    pygame.display.update()
    clock.tick(60)
