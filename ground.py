import pygame
import settings


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.width = settings.screen_width
        self.height = 100
        self.image = pygame.image.load("assets/ground.png")
        self.image = pygame.transform.scale(self.image, (settings.screen_width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
