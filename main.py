import asyncio
import pygame
from sys import exit
import random
import settings
from player import Player
from ground import Ground
from wall import Wall
from texts import Texts


async def main():
    class Game:
        def __init__(self):
            pygame.init()
            self.is_playing = False
            self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
            pygame.display.set_caption("Orbital Cube")
            self.clock = pygame.time.Clock()
            self.start_screen_color = "Red"
            self.game_screen_color = "blue"
            self.scrolling_speed = 5
            self.game_over = False

            # texts setup
            self.texts = Texts()

            # player setup
            self.player = Player()
            self.player.rect.x = settings.screen_width / 3
            self.player_group_single = pygame.sprite.GroupSingle(self.player)

            # wall setup
            self.all_walls = pygame.sprite.Group()
            self.wall = Wall(100, 100, 0, 0, "purple")
            self.wall_start = Wall(settings.screen_width, 300, 0, settings.screen_height - 350, "black")
            self.all_walls.add(self.wall_start)

            # ground setup
            self.ground = Ground(- settings.screen_width / 2, settings.screen_height - 100)
            self.ground_2 = Ground(settings.screen_width / 2, settings.screen_height - 100)
            self.all_grounds = pygame.sprite.Group()

        def events(self):
            for event in pygame.event.get():

                # quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # jump on press space
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.is_playing and self.player.jump_count < 2:
                        self.player.jump()

                # jump on click
                if event.type == pygame.MOUSEBUTTONDOWN and self.is_playing is True and self.player.jump_count < 2:
                    self.player.jump()

                # click on the play button for start game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.texts.play_button_rect.collidepoint(event.pos):
                        self.is_playing = True

                        # reset the score
                        self.texts.score_value = 0

                        # respawn grounds
                        self.all_grounds.add(self.ground, self.ground_2)

            # start player animation
            if self.player.in_the_air is True:
                self.player.animation_on()

            # game over conditions
            if game.player.rect.bottom >= game.ground.rect.top or game.player.rect.left <= 0:
                game.new_game()

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

        def wall_generator(self):

            # generate random color, height and width for the new wall
            random_wall_color = random.choice(self.wall.colors)
            random_wall_height = random.randint(self.wall.wall_height_min, self.wall.wall_height_max)
            random_wall_width = random.randint(self.wall.wall_width_min, self.wall.wall_width_max)

            # generate the first wall
            if len(self.all_walls) < 1:
                self.wall = Wall(random_wall_width, random_wall_height, settings.screen_width, self.ground.rect.top - random_wall_height + 50, random_wall_color)
                self.all_walls.add(self.wall)

            # generate infinite walls
            if self.wall.rect.right <= settings.screen_width - 100:
                self.wall = Wall(random_wall_width, random_wall_height, settings.screen_width, self.ground.rect.top - random_wall_height + 50, random_wall_color)
                self.all_walls.add(self.wall)

            # target the last wall
            first_sprite = self.all_walls.sprites()[0]

            # remove the last wall
            if first_sprite.rect.right <= 0:
                self.all_walls.remove(first_sprite)

                # increase score
                self.texts.score_value += 1

            # remove the start wall
            if self.wall_start.rect.right <= 0:
                self.all_walls.remove(self.wall_start)

        def increase_difficulty(self):
            if self.texts.score_value >= 10:
                self.wall.wall_width_min = 200
                self.wall.wall_width_max = 300
                self.wall.wall_height_min = 300
                self.wall.wall_height_max = 500

        def new_game(self):

            # set game over
            self.game_over = True

            # recreate wall
            self.wall = Wall(100, 100, 0, 0, "purple")

            # player not playing in game over
            self.is_playing = False

            # disable gravity
            self.gravity_off()

            # play the game over sound
            pygame.mixer.music.load('assets/game_over.mp3')
            pygame.mixer.music.play()

            # reset scrolling speed
            self.scrolling_speed = 5

            # replace the player
            self.player.rect.x = settings.screen_width / 3
            self.player.rect.y = 0

            # clear the groups
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
            if self.player.rect.top <= 0:
                self.player.rect.y = 0

            # wall rect collision
            for self.wall in self.all_walls:
                if self.player.rect.colliderect(self.wall.rect):

                    # stop player animation on collision
                    self.player.animation_off()

                    # left wall limits
                    if self.wall.rect.left <= self.player.rect.right <= self.wall.rect.left + 20 and self.player.rect.top >= self.wall.rect.top:
                        self.player.rect.x = self.wall.rect.left - self.player.width

                    # right wall limits
                    if self.wall.rect.right >= self.player.rect.left >= self.wall.rect.right - 20 and self.player.rect.top >= self.wall.rect.top:
                        self.player.rect.x = self.wall.rect.right

                    # top wall limits
                    if self.player.rect.right >= self.wall.rect.left + 20 and self.player.rect.left <= self.wall.rect.right - 20:
                        self.player.rect.y = self.wall.rect.top - self.player.height
                        self.gravity_off()
                        self.player.jump_count = 0
                        self.player.in_the_air = False

            # wall start rect collision
            if self.player.rect.colliderect(self.wall_start.rect):

                if self.player.rect.bottom >= self.wall_start.rect.top:
                    self.player.rect.y = self.wall_start.rect.top - self.player.height
                    self.gravity_off()
                    self.player.jump_count = 0
                    self.player.in_the_air = False

                # stop player animation on collision
                self.player.animation_off()

        def draw(self):
            self.screen.fill(self.game_screen_color)
            self.screen.blit(self.player.image, self.player.rect)
            self.all_grounds.draw(self.screen)
            self.all_walls.draw(self.screen)

        def set_clock(self):
            return self.clock.tick(60)

        def display_score(self):
            score = self.texts.font.render("Score : " + str(self.texts.score_value), True, "white")
            self.screen.blit(score, (30, 30))

        def run(self):

            # start the game
            if game.is_playing is True:
                game.side_scrolling()
                game.collisions()
                game.gravity_on()
                game.draw()
                game.display_score()
                game.increase_difficulty()
                game.wall_generator()
                game.game_over = False
            else:
                # starting screen or game over screen with score
                self.screen.fill(self.start_screen_color)
                self.screen.blit(game.texts.play_button, game.texts.play_button_rect)
                self.screen.blit(self.texts.game_title, self.texts.game_title_rect)

                if game.game_over is True:
                    # change the main text
                    self.texts.game_title = self.texts.font_big.render("Score : " + str(self.texts.score_value), True, "white")
                    self.texts.game_title_rect = self.texts.game_title.get_rect()
                    self.texts.game_title_rect.y = 100
                    self.texts.game_title_rect.centerx = settings.screen_width / 2
                    self.screen.blit(self.texts.game_title, self.texts.game_title_rect)

    game = Game()
    while True:
        game.set_clock()
        game.events()
        game.run()
        pygame.display.update()
        await asyncio.sleep(0)  # Very important, and keep it 0

if __name__ == '__main__':
    asyncio.run(main())
