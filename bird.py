import pygame
from sys import exit

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))  # pygame.image.load()
        self.image.fill((94, 129, 162))
        self.rect = self.image.get_rect(center=(400, 200))
        self.gravity = 0

    def update(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def jump(self):
        self.gravity = -15

pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Flappy Bird')
bird = Bird()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    screen.fill((0, 0, 0))

    bird.update()
    screen.blit(bird.image, bird.rect)

    pygame.display.update()
    clock.tick(60)
