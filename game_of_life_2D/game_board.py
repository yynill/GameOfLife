import math
import pygame


class GameBoard:
    def __init__(self):
        self.num_of_tiles = 10
        self.tile_size = math.floor(800/self.num_of_tiles)
        self.board_height = self.num_of_tiles * self.tile_size
        self.board_width = self.board_height
        self.tiles = [
            [0] * self.num_of_tiles for _ in range(self.num_of_tiles)]

        self.window = pygame.display.set_mode(
            (self.board_width, self.board_height))
        pygame.display.set_caption('game of life')

        pygame.display.flip()

    def paint_tile(self, mouse_x, mouse_y):
        row = mouse_y // self.tile_size
        col = mouse_x // self.tile_size
        self.tiles[row][col] = 1

    def remove_tile(self, mouse_x, mouse_y):
        row = mouse_y // self.tile_size
        col = mouse_x // self.tile_size
        self.tiles[row][col] = 0

    def draw_tiles(self):
        for col in range(self.num_of_tiles):
            for row in range(self.num_of_tiles):
                if self.tiles[row][col] == 1:
                    pygame.draw.rect(self.window, (255, 255, 255),
                                     (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.tiles[row][col] == 2:
                    pygame.draw.rect(self.window,  (255, 255, 255),
                                     (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.window, (35, 35, 35),
                                     (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size), 1)

    def update_tiles(self):
        new_tiles = [[0] * self.num_of_tiles for _ in range(self.num_of_tiles)]

        for col in range(self.num_of_tiles):
            for row in range(self.num_of_tiles):
                count = 0
                for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    new_row = row + i
                    new_col = col + j
                    if 0 <= new_row < len(self.tiles) and 0 <= new_col < len(self.tiles[0]):
                        if self.tiles[new_row][new_col] != 0:
                            count += 1

                current_state = self.tiles[row][col]

                # Birth rule
                if current_state == 0 and count == 3:
                    new_tiles[row][col] = 1

                # Death rule
                elif (current_state != 0) and (count <= 1 or count >= 4):
                    new_tiles[row][col] = 0

                # Survival rule
                elif (current_state != 0) and (count == 2 or count == 3):
                    new_tiles[row][col] = 2

        self.tiles = new_tiles

    def reset(self):
        self.tiles = [
            [0] * self.num_of_tiles for _ in range(self.num_of_tiles)]

    def draw_window(self, pause):
        if pause:
            self.window.fill((0, 0, 0))
            self.draw_tiles()
        else:
            self.window.fill((0, 0, 0))
            self.update_tiles()
            self.draw_tiles()

        pygame.display.flip()
