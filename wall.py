import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.main_color = (242, 34, 255)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.wall_width_min = 100
        self.wall_width_max = 500
        self.wall_height_min = 50
        self.wall_height_max = 250
        self.wall_separator = 150
