import pygame


class SoundManager:

    def __init__(self):
        self.sounds = {
            'jump': pygame.mixer.Sound("assets/jump.mp3"),
            'game_over': pygame.mixer.Sound("assets/game_over.mp3"),
            'on_ground': pygame.mixer.Sound("assets/on_ground.mp3")
        }

    def play(self, name):
        self.sounds[name].play()
