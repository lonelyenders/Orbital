import pygame


pygame.init()

'''
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
'''

screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# game screen title
pygame.display.set_caption("The Wall")

# FPS settings
clock = pygame.time.Clock()
