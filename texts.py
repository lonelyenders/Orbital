import pygame
import settings


class Texts:
    def __init__(self):
        self.score_value = 0

        self.font = pygame.font.Font('assets/amity.ttf', int(settings.screen_width / 20))
        self.font_big = pygame.font.Font('assets/amity.ttf', int(settings.screen_width / 10))
        self.game_title = self.font_big.render("Orbital Cube", True, "white")
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.y = 130
        self.game_title_rect.centerx = settings.screen_width / 2

        self.help_title = self.font.render("Press SPACE or CLICK to JUMP", True, "white")
        self.help_title_rect = self.help_title.get_rect()
        self.help_title_rect.y = 150
        self.help_title_rect.centerx = settings.screen_width / 2

        self.play_button = pygame.image.load("assets/play.png")
        self.play_button = pygame.transform.scale(self.play_button, (150, 75))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.centerx = settings.screen_width / 2
        self.play_button_rect.y = self.game_title_rect.bottom
        self.main_font_color = (255, 41, 117)
