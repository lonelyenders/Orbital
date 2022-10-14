import pygame
from sys import exit
import random
import settings
from player import Player
from ground import Ground
from wall import Wall
from sounds import SoundManager


class Game:
    def __init__(self):

        # game loop settings
        self.running = True
        self.is_playing = False

        # setup backgrounds
        self.background_color = (152, 136, 177)
        self.background_image = pygame.image.load("assets/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (settings.screen_width, settings.screen_height))

        self.play_button = pygame.image.load("assets/play.png")
        self.play_button = pygame.transform.scale(self.play_button, (150, 75))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = settings.screen_width / 2 - self.play_button_rect.width / 2
        self.play_button_rect.y = 250

        # sound setup
        self.sound_manager = SoundManager()

        # scoring setup
        self.score_value = 0

        # scrolling speed
        self.scrolling_speed = 5

        # delay
        self.current_time = 0

        # font and text setup
        # self.font = pygame.font.SysFont('Arial Black', 30)
        self.font = pygame.font.Font('assets/atos.otf', 50)
        self.font_big = pygame.font.Font('assets/atos.otf', 60)
        self.game_title = self.font_big.render("Metacube", True, "white")
        self.game_title_rect = self.game_title.get_rect()
        self.game_title_rect.x = settings.screen_width / 2 - self.game_title_rect.width / 2
        self.game_title_rect.y = 150

        # player setup
        self.player = Player()
        self.player.rect.x = settings.screen_width / 3

        # grounds setup
        self.ground = Ground(- settings.screen_width / 2, settings.screen_height - 100)
        self.ground_2 = Ground(settings.screen_width / 2, settings.screen_height - 100)

        # walls setup
        self.wall = Wall(100, 100, 0, 0, "purple")
        self.wall_start = Wall(settings.screen_width, 300, 0, settings.screen_height - 350, "black")

        # groups setup
        self.player_group_single = pygame.sprite.GroupSingle(self.player)
        self.all_grounds = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()

        # create the start wall
        self.all_walls.add(self.wall_start)

    def events(self):
        for event in pygame.event.get():

            # quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.jump_count < 2:
                    self.player.jump()
                    self.sound_manager.play("jump")

            if event.type == pygame.MOUSEBUTTONDOWN and self.is_playing is True and self.player.jump_count < 2:
                self.player.jump()
                self.sound_manager.play("jump")

            # click on the play button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.is_playing = True

                    # respawn walls and grounds
                    self.all_grounds.add(self.ground, self.ground_2)

    def game_loop(self):
        while self.running is True:

            self.events()

            # start the game
            if self.is_playing is True:
                self.side_scrolling()
                self.collisions()
                self.gravity_on()
                self.draw()
                self.display_score()
                self.player.animation_on()
                self.increase_difficulty()
                self.wall_generator()

                # delay
                self.current_time = pygame.time.get_ticks()

                # game over
                if self.player.rect.bottom >= self.ground.rect.top or self.player.rect.left <= 0:
                    self.game_over()

                # display score after game over
                if self.score_value > 0:
                    self.game_title = self.font_big.render("Score : " + str(self.score_value), True, "white")

            else:
                # starting screen or game over screen with score
                settings.screen.blit(self.background_image, (0, 0))
                settings.screen.blit(self.play_button, self.play_button_rect)
                settings.screen.blit(self.game_title, self.game_title_rect)

            # update the game
            self.update()

    def wall_generator(self):

        random_wall_color = random.choice(self.wall.colors)
        random_wall_height = random.randint(self.wall.wall_height_min, self.wall.wall_height_max)
        random_wall_width = random.randint(self.wall.wall_width_min, self.wall.wall_width_max)

        if len(self.all_walls) < 1:
            self.wall = Wall(random_wall_width, random_wall_height, settings.screen_width, self.ground.rect.top - random_wall_height + 50, random_wall_color)
            self.all_walls.add(self.wall)

        if self.wall.rect.right <= settings.screen_width - random_wall_width:
            self.wall = Wall(random_wall_width, random_wall_height, settings.screen_width, self.ground.rect.top - random_wall_height + 50, random_wall_color)
            self.all_walls.add(self.wall)

        first_sprite = self.all_walls.sprites()[0]

        if first_sprite.rect.right <= 0:
            self.all_walls.remove(first_sprite)

            # increase score
            self.score_value += 1

        # remove start wall
        if self.wall_start.rect.right <= 0:
            self.all_walls.remove(self.wall_start)

    def side_scrolling(self):
        # ground scrolling
        self.ground.rect.x -= self.scrolling_speed
        self.ground_2.rect.x -= self.scrolling_speed

        # wall scrolling
        for self.wall in self.all_walls:
            self.wall.rect.x -= self.scrolling_speed

        # ground respawn
        if self.ground.rect.right <= 0:
            self.ground.rect.x = settings.screen_width

        if self.ground_2.rect.right <= 0:
            self.ground_2.rect.x = settings.screen_width

    def increase_difficulty(self):
        if self.score_value >= 10:
            self.wall.wall_width_min = 100
            self.wall.wall_width_max = 150

        if self.score_value >= 20:
            self.wall.wall_height_min = 100
            self.wall.wall_height_max = 300

    def display_score(self):
        score = self.font.render("Score : " + str(self.score_value), True, "white")
        settings.screen.blit(score, (30, 30))

    def game_over(self):

        # recreate wall
        self.wall = Wall(100, 100, 0, 0, "purple")

        # player not playing in game over
        self.is_playing = False

        # disable gravity
        self.gravity_off()

        # play the game over sound
        self.sound_manager.play("game_over")

        # reset the score
        self.score_value = 0

        # reset scrolling speed
        self.scrolling_speed = 5

        # replace the player
        self.player.rect.x = settings.screen_width / 3
        self.player.rect.y = 0

        # despawn
        self.all_walls.empty()
        self.all_grounds.empty()

        # replace grounds
        self.ground = Ground(- settings.screen_width / 2, settings.screen_height - 100)
        self.ground_2 = Ground(settings.screen_width / 2, settings.screen_height - 100)

        # replace the start wall
        self.wall_start = Wall(settings.screen_width, 300, 0, settings.screen_height - 350, "red")
        self.all_walls.add(self.wall_start)

    def gravity_on(self):
        self.player.gravity += 1
        self.player.rect.y += self.player.gravity

    def gravity_off(self):
        self.player.gravity = 0

    def collisions(self):

        # player collisions with the screen
        if self.player.rect.right >= settings.screen_width:
            self.player.rect.x = settings.screen_width - self.player.width

        if self.player.rect.left <= 0:
            self.player.rect.x = 0

        if self.player.rect.top <= 0:
            self.player.rect.y = 0

        # bottom screen collision for debug
        if self.player.rect.bottom >= self.ground.rect.top:
            self.player.rect.y = self.ground.rect.top

        # wall collisions
        if pygame.sprite.groupcollide(self.player_group_single, self.all_walls, False, False):

            for self.wall in self.all_walls:

                # stop player animation if collide
                self.player.animation_off()

                # left wall limits
                if self.wall.rect.left <= self.player.rect.right <= self.wall.rect.left + 20 and self.player.rect.top >= self.wall.rect.top:
                    self.player.rect.x = self.wall.rect.left - self.player.width

                # right wall limits
                if self.wall.rect.right >= self.player.rect.left >= self.wall.rect.right - 20 and self.player.rect.top >= self.wall.rect.top:
                    self.player.rect.x = self.wall.rect.right

                # top wall limits
                if self.player.rect.right >= self.wall.rect.left + 10 and self.player.rect.left <= self.wall.rect.right - 10:
                    self.player.rect.y = self.wall.rect.top - self.player.height

                    # stop gravity on a wall
                    self.gravity_off()

                    # reset jump count
                    self.player.jump_count = 0

    def draw(self):
        settings.screen.fill(self.background_color)
        settings.screen.blit(self.player.image, self.player.rect)
        # settings.screen.blit(self.ground.image, self.ground.rect)
        self.all_grounds.draw(settings.screen)
        self.all_walls.draw(settings.screen)

    def update(self):
        pygame.display.update()
        self.set_clock()

    def set_clock(self):
        return settings.clock.tick(60)
