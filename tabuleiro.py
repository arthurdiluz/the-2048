import pygame
from pygame.locals import *
from random import random
from math import floor
from cores import *


class Matriz:
    def __init__(self, superficie: pygame.display, blocos_matriz: list, desfazer_jogada: list,
                 fonte: pygame.font, placar_fonte: pygame.font):
        self.superficie = superficie
        self.bloco_matriz = blocos_matriz
        self.desfazer_jogada = desfazer_jogada
        self.fonte = fonte
        self.placar_fonte = placar_fonte
        self.tot_pontos = 0
        self.placar_padrao = 2
        self.placa_tam = 4
        self.cor = Cores()

    def exibir_matriz(self):
        self.superficie.fill(self.cor.preto)

        for i in range(self.placa_tam):
            for j in range(self.placa_tam):
                pygame.draw.rect(
                    self.superficie,
                    self.cor.obter_cor(self.bloco_matriz[i][j]),
                    (i * (400 / self.placa_tam), j * (400 / self.placa_tam) + 100, 400 / self.placa_tam,
                     400 / self.placa_tam)
                )

                placar = self.fonte.render(str(self.bloco_matriz[i][j]), 1, self.cor.branco)
                pontuacao = self.placar_fonte.render("Pontuação:" + str(self.tot_pontos), 1, self.cor.branco)

                self.superficie.blit(placar, (i * (400 / self.placa_tam) + 30, j * (400 / self.placa_tam) + 130))
                self.superficie.blit(pontuacao, (10, 20))

    def exibir_gameover(self):
        self.superficie.fill(self.cor.preto)
        self.superficie.blit(self.placar_fonte.render("FIM DE JOGO!", 1, self.cor.branco), (50, 100))
        self.superficie.blit(self.placar_fonte.render("Pontos: " + str(self.tot_pontos), 1, self.cor.branco), (50, 200))
        self.superficie.blit(self.fonte.render("Pressione R para reiniciar!", 1, self.cor.branco), (30, 400))

    def posicionar_bloco(self, contador=0):
        for i in range(self.placa_tam):
            for j in range(self.placa_tam):
                if self.bloco_matriz[i][j] == 0:
                    contador += 1

        k = floor(random() * self.placa_tam * self.placa_tam)  # lugar aleatório na matriz

        # procura um lugar vazio na matriz
        while self.bloco_matriz[floor(k / self.placa_tam)][k % self.placa_tam] != 0:
            k = floor(random() * self.placa_tam * self.placa_tam)

        # coloca na matriz na posição encontrada
        self.bloco_matriz[floor(k / self.placa_tam)][k % self.placa_tam] = 2

    def mover_bloco(self):
        for i in range(self.placa_tam):
            for j in range(self.placa_tam - 1):
                while self.bloco_matriz[i][j] == 0 and sum(self.bloco_matriz[i][j:]) > 0:
                    for k in range(j, self.placa_tam - 1):
                        self.bloco_matriz[i][k] = self.bloco_matriz[i][k + 1]
                    self.bloco_matriz[i][self.placa_tam - 1] = 0

    def mesclar_blocos(self):
        for i in range(self.placa_tam):
            for k in range(self.placa_tam - 1):
                if self.bloco_matriz[i][k] == self.bloco_matriz[i][k + 1] and self.bloco_matriz[i][k] != 0:
                    self.bloco_matriz[i][k] = self.bloco_matriz[i][k] * 2
                    self.bloco_matriz[i][k + 1] = 0
                    self.tot_pontos += self.bloco_matriz[i][k]
                    self.mover_bloco()

    def checar_ir(self):
        for i in range(pow(self.placa_tam, 2)):
            if self.bloco_matriz[floor(i / self.placa_tam)][i % self.placa_tam] == 0:
                return True

        for i in range(self.placa_tam):
            for j in range(self.placa_tam - 1):
                if self.bloco_matriz[i][j] == self.bloco_matriz[i][j + 1]:
                    return True
                elif self.bloco_matriz[j][i] == self.bloco_matriz[j + 1][i]:
                    return True
        return False

    def reiniciar(self):
        self.tot_pontos = 0
        self.superficie.fill(self.cor.preto)
        self.bloco_matriz = [[0 for i in range(self.placa_tam)] for j in range(self.placa_tam)]

    def pode_mover(self):
        for i in range(self.placa_tam):
            for j in range(1, self.placa_tam):
                if self.bloco_matriz[i][j - 1] == 0 and self.bloco_matriz[i][j] > 0:
                    return True
                elif (self.bloco_matriz[i][j - 1] == self.bloco_matriz[i][j]) and self.bloco_matriz[i][j - 1] != 0:
                    return True
        return False

    def rotacionar_matriz(self):
        for i in range(int(self.placa_tam / 2)):
            for k in range(i, self.placa_tam - i - 1):
                temp1 = self.bloco_matriz[i][k]
                temp2 = self.bloco_matriz[self.placa_tam - 1 - k][i]
                temp3 = self.bloco_matriz[self.placa_tam - 1 - i][self.placa_tam - 1 - k]
                temp4 = self.bloco_matriz[k][self.placa_tam - 1 - i]

                self.bloco_matriz[self.placa_tam - 1 - k][i] = temp1
                self.bloco_matriz[self.placa_tam - 1 - i][self.placa_tam - 1 - k] = temp2
                self.bloco_matriz[k][self.placa_tam - 1 - i] = temp3
                self.bloco_matriz[i][k] = temp4

    def converter_matriz_linear(self):
        mat = []

        for i in range(self.placa_tam ** 2):
            mat.append(self.bloco_matriz[floor(i / self.placa_tam)][i % self.placa_tam])
        mat.append(self.tot_pontos)

        return mat

    def add_desfazer(self):
        self.desfazer_jogada.append(self.converter_matriz_linear())

    def desfazer(self):
        if len(self.desfazer_jogada) > 0:
            mat = self.desfazer_jogada.pop()

            for i in range(self.placa_tam ** 2):
                self.bloco_matriz[floor(i / self.placa_tam)][i % self.placa_tam] = mat[i]

            self.tot_pontos = mat[self.placa_tam ** 2]
            self.exibir_matriz()

    def setas(self, tecla):
        return tecla == pygame.K_UP or tecla == pygame.K_DOWN or tecla == pygame.K_LEFT or tecla == pygame.K_RIGHT

    def obter_rotacao(self, tecla):
        if tecla == pygame.K_UP:
            return 0
        elif tecla == pygame.K_DOWN:
            return 2
        elif tecla == pygame.K_LEFT:
            return 1
        elif tecla == pygame.K_RIGHT:
            return 3