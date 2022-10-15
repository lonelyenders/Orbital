import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.colors = [(17, 17, 17), (39, 39, 47), (48, 48, 56), (41, 41, 41), (57, 45, 47)]
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.wall_width_min = 100
        self.wall_width_max = 200
        self.wall_height_min = 200
        self.wall_height_max = 400
