import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.width = 1080
        self.height = 100
        self.image = pygame.image.load("assets/ground.png")
        self.image = pygame.transform.scale(self.image, (1080, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
