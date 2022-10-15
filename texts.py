import pygame
import settings


class Texts:
    def __init__(self):
        self.score_value = 0

        self.font = pygame.font.Font('assets/atos.otf', int(settings.screen_width / 20))
        self.font_big = pygame.font.Font('assets/atos.otf', int(settings.screen_width / 10))
        self.game_title = self.font_big.render("Orbital Cube", True, "white")
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.y = 100
        self.game_title_rect.centerx = settings.screen_width / 2
        self.play_button = pygame.image.load("assets/play.png")
        self.play_button = pygame.transform.scale(self.play_button, (150, 75))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.centerx = settings.screen_width / 2
        self.play_button_rect.y = self.game_title_rect.bottom
