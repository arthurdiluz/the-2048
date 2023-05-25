import pygame
from src.classes.table import Table
from pygame.constants import QUIT, KEYDOWN
import sys


def main(is_loaded=False):
    if not is_loaded:
        board.place_block()
        board.place_block()
    board.display_table()

    while True:
        for event in pygame.event.get():  # lista de eventos
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if board.check_go():
                if event.type == KEYDOWN:
                    if board.arrows(event.key):
                        rotations = board.get_rotation(event.key)
                        board.add_undo()

                        for i in range(rotations):
                            board.rotate_table()

                        if board.can_move():
                            board.move_block()
                            board.merge_blocks()
                            board.place_block()

                        for j in range((4 - rotations) % 4):
                            board.rotate_table()
                        board.display_table()
            else:
                board.display_game_over()

            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    board.restart()
                    main()
                if event.key == pygame.K_u:
                    board.undo()
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("The 2048")
    pygame.display.set_icon(pygame.image.load("img/icon.png"))

    board = Table(
        pygame.display.set_mode((400, 500), 0, 32),
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [],
        pygame.font.SysFont("monospace", 22),
        pygame.font.SysFont("monospace", 42),
    )

    main()
    exit()
