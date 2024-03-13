import pygame
from game_board import GameBoard


def main():
    pygame.init()

    game_board = GameBoard()

    running = True
    clock = pygame.time.Clock()
    pause = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_board.reset()
                elif event.key == pygame.K_SPACE:
                    pause = not pause
                    print(pause)

            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_board.paint_tile(*event.pos)
                    elif event.button == 3:
                        game_board.remove_tile(*event.pos)

        game_board.draw_window(pause)

    pygame.quit()


if __name__ == "__main__":
    main()
