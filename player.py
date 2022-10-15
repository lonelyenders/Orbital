import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.image.load("assets/cube_blue.png")
        self.origin_image = self.image
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.gravity = 0
        self.velocity = 10
        self.jump_height = 20
        self.jump_count = 0
        self.in_the_air = False

    def jump(self):
        self.gravity = - self.jump_height
        self.rect.y -= self.jump_height
        self.jump_count += 1
        self.in_the_air = True
        pygame.mixer.music.load('assets/swing.mp3')
        pygame.mixer.music.play()

    def animation_on(self):
        self.angle -= self.velocity
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def animation_off(self):
        self.image = pygame.transform.rotozoom(self.origin_image, 0, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
