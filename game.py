import pygame
import sys
import random
from maze import Maze
from utils.maze_list import MAZE_LIST
from bullet import Bullet
from tank import Tank
from utils.colors import WHITE, RED, COLORS
from utils.sizes import BLOCK_SIZE, MAZE_WIDTH, MAZE_HEIGHT
from sfx import shoot_sound_effect
from utils.menu import draw_menu
from time import time

pygame.init()
# maze pattern
pattern = random.choice(MAZE_LIST)
# map color
maze_color = random.choice(COLORS)
bg_color = random.choice(COLORS)

while bg_color == maze_color or bg_color == COLORS[0]:
    bg_color = random.choice(COLORS)


def quit_game():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        # screen settings
        self.width = MAZE_WIDTH * BLOCK_SIZE
        self.mid_w = self.width // 2
        self.height = MAZE_HEIGHT * BLOCK_SIZE
        self.mid_h = self.height // 2
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Combat - Tank (Atari 2600)")
        # game controls
        self.game_start = False
        self.show_credits = False
        self.clock = pygame.time.Clock()
        # maze
        self.maze = Maze(pattern, maze_color)
        # tanks
        self.tank1 = Tank(1, 1, WHITE, BLOCK_SIZE, 1, self.maze.walls)
        self.tank1_initial_time = time()
        self.tank1_final_time = time()
        self.tank2 = Tank(MAZE_WIDTH - 2, MAZE_HEIGHT - 2, WHITE, BLOCK_SIZE, 2, self.maze.walls)
        self.tank2_initial_time = time()
        self.tank2_final_time = time()
        # bullet and sprite groups
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank1, self.tank2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                # handle shooting
                if self.game_start:
                    if event.key == pygame.K_SPACE:
                        self.fire_bullet(self.tank1)
                    elif event.key == pygame.K_RETURN:
                        self.fire_bullet(self.tank2)
                # handle menu screen events
                elif not self.game_start:
                    if event.key == pygame.K_SPACE and not self.show_credits:
                        self.game_start = True
                    elif event.key == pygame.K_RETURN:
                        self.show_credits = not self.show_credits

    def update(self):
        # tanks dir
        self.tank1.draw_pointer(self.screen)
        self.tank2.draw_pointer(self.screen)
        # tanks shoot waiting
        self.tank1_final_time = time()
        self.tank2_final_time = time()
        # update all
        self.all_sprites.update(self.maze.walls, self.bullets)

    def draw_game(self):
        self.screen.fill(bg_color)
        self.maze.draw(self.screen)
        # draw tank and bullets
        self.all_sprites.draw(self.screen)

    def fire_bullet(self, tank):
        # handle bullet dir based on tank
        if tank == self.tank1:
            if self.tank1_final_time - self.tank1_initial_time > 2:
                bullet_direction = (self.tank1.block_dx / 3, self.tank1.block_dy / 3)
                self.tank1_initial_time = time()
                bullet = Bullet(tank.rect_block.centerx, tank.rect_block.centery, bullet_direction, RED)
                shoot_sound_effect.play()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        elif tank == self.tank2:
            if self.tank2_final_time - self.tank2_initial_time > 2:
                bullet_direction = (self.tank2.block_dx / 3, self.tank2.block_dy / 3)
                bullet = Bullet(tank.rect_block.centerx, tank.rect_block.centery, bullet_direction, RED)
                self.tank2_initial_time = time()
                shoot_sound_effect.play()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

    def run(self):
        running = True
        while running:
            if self.game_start:
                self.draw_game()
            else:
                draw_menu(self.screen, self.show_credits, self.mid_w, self.mid_h)
            self.update()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(60)
