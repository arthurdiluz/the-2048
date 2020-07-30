import pygame
from random import random
from math import floor
from src.classes.colors import *


class Table:
    def __init__(self, surface: pygame.display, matrix_block: list, undo_play: list,
                 font: pygame.font, scoreboard_font: pygame.font):
        self.surface = surface
        self.matrix_block = matrix_block
        self.undo_play = undo_play
        self.font = font
        self.scoreboard_font = scoreboard_font
        self.total_points = 0
        self.default_scoreboard = 2
        self.scoreboard_size = 4
        self.color = Colors()

    def display_table(self):
        self.surface.fill(self.color.black)

        for i in range(self.scoreboard_size):
            for j in range(self.scoreboard_size):
                pygame.draw.rect(
                    self.surface,
                    self.color.get_color(self.matrix_block[i][j]),
                    (i * (400 / self.scoreboard_size),
                     j * (400 / self.scoreboard_size) + 100,
                     400 / self.scoreboard_size,
                     400 / self.scoreboard_size)
                )

                scoreboard = self.font.render(str(self.matrix_block[i][j]), 1, self.color.white)
                score = self.scoreboard_font.render("Score:" + str(self.total_points), 1, self.color.white)

                self.surface.blit(
                    scoreboard,
                    (i * (400 / self.scoreboard_size) + 30,
                     j * (400 / self.scoreboard_size) + 130)
                )
                self.surface.blit(score, (10, 20))

    def display_game_over(self):
        self.surface.fill(self.color.black)
        self.surface.blit(self.scoreboard_font.render("THE END!", 1, self.color.white), (50, 100))
        self.surface.blit(self.scoreboard_font.render(
            "Score: " + str(self.total_points),
            1,
            self.color.white),
            (50, 200)
        )
        self.surface.blit(self.font.render("Press R to restart!", 1, self.color.white), (30, 400))

    def place_block(self, count=0):
        for i in range(self.scoreboard_size):
            for j in range(self.scoreboard_size):
                if self.matrix_block[i][j] == 0:
                    count += 1

        k = floor(random() * self.scoreboard_size * self.scoreboard_size)  # random place on matrix

        # seeks an empty place on matrix
        while self.matrix_block[floor(k / self.scoreboard_size)][k % self.scoreboard_size] != 0:
            k = floor(random() * self.scoreboard_size * self.scoreboard_size)

        # adds element on matrix at found place
        self.matrix_block[floor(k / self.scoreboard_size)][k % self.scoreboard_size] = 2

    def move_block(self):
        for i in range(self.scoreboard_size):
            for j in range(self.scoreboard_size - 1):
                while self.matrix_block[i][j] == 0 and sum(self.matrix_block[i][j:]) > 0:
                    for k in range(j, self.scoreboard_size - 1):
                        self.matrix_block[i][k] = self.matrix_block[i][k + 1]
                    self.matrix_block[i][self.scoreboard_size - 1] = 0

    def merge_blocks(self):
        for i in range(self.scoreboard_size):
            for k in range(self.scoreboard_size - 1):
                if self.matrix_block[i][k] == self.matrix_block[i][k + 1] and self.matrix_block[i][k] != 0:
                    self.matrix_block[i][k] = self.matrix_block[i][k] * 2
                    self.matrix_block[i][k + 1] = 0
                    self.total_points += self.matrix_block[i][k]
                    self.move_block()

    def check_go(self):
        for i in range(pow(self.scoreboard_size, 2)):
            if self.matrix_block[floor(i / self.scoreboard_size)][i % self.scoreboard_size] == 0:
                return True

        for i in range(self.scoreboard_size):
            for j in range(self.scoreboard_size - 1):
                if self.matrix_block[i][j] == self.matrix_block[i][j + 1]:
                    return True
                elif self.matrix_block[j][i] == self.matrix_block[j + 1][i]:
                    return True
        return False

    def restart(self):
        self.total_points = 0
        self.surface.fill(self.color.black)
        self.matrix_block = [[0 for _ in range(self.scoreboard_size)] for _ in range(self.scoreboard_size)]

    def can_move(self):
        for i in range(self.scoreboard_size):
            for j in range(1, self.scoreboard_size):
                if self.matrix_block[i][j - 1] == 0 and self.matrix_block[i][j] > 0:
                    return True
                elif (self.matrix_block[i][j - 1] == self.matrix_block[i][j]) and self.matrix_block[i][j - 1] != 0:
                    return True
        return False

    def rotate_table(self):
        for i in range(int(self.scoreboard_size / 2)):
            for k in range(i, self.scoreboard_size - i - 1):
                temp1 = self.matrix_block[i][k]
                temp2 = self.matrix_block[self.scoreboard_size - 1 - k][i]
                temp3 = self.matrix_block[self.scoreboard_size - 1 - i][self.scoreboard_size - 1 - k]
                temp4 = self.matrix_block[k][self.scoreboard_size - 1 - i]

                self.matrix_block[self.scoreboard_size - 1 - k][i] = temp1
                self.matrix_block[self.scoreboard_size - 1 - i][self.scoreboard_size - 1 - k] = temp2
                self.matrix_block[k][self.scoreboard_size - 1 - i] = temp3
                self.matrix_block[i][k] = temp4

    def convert_linear_matrix(self):
        mat = []

        for i in range(self.scoreboard_size ** 2):
            mat.append(self.matrix_block[floor(i / self.scoreboard_size)][i % self.scoreboard_size])
        mat.append(self.total_points)

        return mat

    def add_undo(self):
        self.undo_play.append(self.convert_linear_matrix())

    def undo(self):
        if len(self.undo_play) > 0:
            mat = self.undo_play.pop()

            for i in range(self.scoreboard_size ** 2):
                self.matrix_block[floor(i / self.scoreboard_size)][i % self.scoreboard_size] = mat[i]

            self.total_points = mat[self.scoreboard_size ** 2]
            self.display_table()

    @staticmethod
    def arrows(key):
        return key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT

    @staticmethod
    def get_rotation(key):
        if key == pygame.K_UP:
            return 0
        elif key == pygame.K_DOWN:
            return 2
        elif key == pygame.K_LEFT:
            return 1
        elif key == pygame.K_RIGHT:
            return 3
