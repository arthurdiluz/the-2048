import pygame
import sys
from pygame.locals import *
from random import random
from math import floor
from colours import *


def main(esta_carregado=False):

    if not esta_carregado:
        posicionar_bloco()
        posicionar_bloco()

    exibir_matriz()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if checar_ir():
                if event.type == KEYDOWN:
                    if setas(event.key):
                        rotations = obter_rotacao(event.key)

                        add_desfazer()

                        for i in range(0, rotations):
                            rotacionar_matriz()

                        if pode_mover():
                            mover_bloco()
                            mesclar_blocos()
                            posicionar_bloco()

                        for j in range(0, (4 - rotations) % 4):
                            rotacionar_matriz()

                        exibir_matriz()
            else:
                exibir_gameover()

            if event.type == KEYDOWN:
                global placa_tamanho

                if event.key == pygame.K_r:
                    reiniciar()

                if 50 < event.key < 56:
                    placa_tamanho = event.key - 48
                    reiniciar()

                elif event.key == pygame.K_u:
                    desfazer()

        pygame.display.update()


def exibir_matriz():
    superficie.fill(cor.preto)

    global placa_tamanho
    global pontos_totais
    
    for i in range(placa_tamanho):
        for j in range(placa_tamanho):
            pygame.draw.rect(
                superficie,
                cor.obter_cor(bloco_matriz[i][j]),
                (i * (400 / placa_tamanho), j * (400 / placa_tamanho) + 100, 400 / placa_tamanho, 400 / placa_tamanho)
            )

            label = fonte.render(str(bloco_matriz[i][j]), 1, (255, 255, 255))
            label2 = placar_fonte.render("Score:" + str(pontos_totais), 1, (255, 255, 255))

            superficie.blit(label, (i * (400 / placa_tamanho) + 30, j * (400 / placa_tamanho) + 130))
            superficie.blit(label2, (10, 20))


def exibir_gameover():
    global pontos_totais

    superficie.fill(cor.preto)

    label = placar_fonte.render("Game Over!", 1, (255, 255, 255))
    label2 = placar_fonte.render("Score:" + str(pontos_totais), 1, (255, 255, 255))
    label3 = fonte.render("Press r to restart!", 1, (255, 255, 255))

    superficie.blit(label, (50, 100))
    superficie.blit(label2, (50, 200))
    superficie.blit(label3, (50, 300))


def posicionar_bloco():
    count = 0
    for i in range(0, placa_tamanho):
        for j in range(0, placa_tamanho):
            if bloco_matriz[i][j] == 0:
                count += 1

    k = floor(random() * placa_tamanho * placa_tamanho)

    while bloco_matriz[floor(k / placa_tamanho)][k % placa_tamanho] != 0:
        k = floor(random() * placa_tamanho * placa_tamanho)

    bloco_matriz[floor(k / placa_tamanho)][k % placa_tamanho] = 2


def mover_bloco():
    for i in range(0, placa_tamanho):
        for j in range(placa_tamanho - 1):
            while bloco_matriz[i][j] == 0 and sum(bloco_matriz[i][j:]) > 0:
                for k in range(j, placa_tamanho - 1):
                    bloco_matriz[i][k] = bloco_matriz[i][k + 1]
                bloco_matriz[i][placa_tamanho - 1] = 0


def mesclar_blocos():
    global pontos_totais

    for i in range(placa_tamanho):
        for k in range(placa_tamanho - 1):
            if bloco_matriz[i][k] == bloco_matriz[i][k + 1] and bloco_matriz[i][k] != 0:
                bloco_matriz[i][k] = bloco_matriz[i][k] * 2
                bloco_matriz[i][k + 1] = 0
                pontos_totais += bloco_matriz[i][k]
                mover_bloco()


def checar_ir():
    for i in range(0, placa_tamanho ** 2):
        if bloco_matriz[floor(i / placa_tamanho)][i % placa_tamanho] == 0:
            return True

    for i in range(0, placa_tamanho):
        for j in range(0, placa_tamanho - 1):
            if bloco_matriz[i][j] == bloco_matriz[i][j + 1]:
                return True
            elif bloco_matriz[j][i] == bloco_matriz[j + 1][i]:
                return True
    return False


def reiniciar():
    global pontos_totais
    global bloco_matriz

    pontos_totais = 0
    superficie.fill(cor.preto)

    bloco_matriz = [[0 for i in range(0, placa_tamanho)] for j in range(0, placa_tamanho)]

    main()


def pode_mover():
    for i in range(0, placa_tamanho):
        for j in range(1, placa_tamanho):
            if bloco_matriz[i][j - 1] == 0 and bloco_matriz[i][j] > 0:
                return True
            elif (bloco_matriz[i][j - 1] == bloco_matriz[i][j]) and bloco_matriz[i][j - 1] != 0:
                return True

    return False


def rotacionar_matriz():
    for i in range(0, int(placa_tamanho / 2)):
        for k in range(i, placa_tamanho - i - 1):
            temp1 = bloco_matriz[i][k]
            temp2 = bloco_matriz[placa_tamanho - 1 - k][i]
            temp3 = bloco_matriz[placa_tamanho - 1 - i][placa_tamanho - 1 - k]
            temp4 = bloco_matriz[k][placa_tamanho - 1 - i]

            bloco_matriz[placa_tamanho - 1 - k][i] = temp1
            bloco_matriz[placa_tamanho - 1 - i][placa_tamanho - 1 - k] = temp2
            bloco_matriz[k][placa_tamanho - 1 - i] = temp3
            bloco_matriz[i][k] = temp4


def setas(k):
    return k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT


def obter_rotacao(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


def converter_matriz_linear():
    mat = []

    for i in range(0, placa_tamanho ** 2):
        mat.append(bloco_matriz[floor(i / placa_tamanho)][i % placa_tamanho])  # ESTRUTURA DE DADOS

    mat.append(pontos_totais)  # ESTRUTURA DE DADOS

    return mat


def add_desfazer():
    desfazer_jogada.append(converter_matriz_linear())  # ESTRUTURA DE DADOS


def desfazer():
    if len(desfazer_jogada) > 0:
        mat = desfazer_jogada.pop()  # ESTRUTURA DE DADOS

        for i in range(0, placa_tamanho ** 2):
            bloco_matriz[floor(i / placa_tamanho)][i % placa_tamanho] = mat[i]

        global pontos_totais
        pontos_totais = mat[placa_tamanho ** 2]

        exibir_matriz()


if __name__ == '__main__':
    pontos_totais = 0
    placar_padrao = 2
    placa_tamanho = 4

    pygame.init()
    cor = Cores()

    superficie = pygame.display.set_mode((400, 500), 0, 32)
    pygame.display.set_caption("O JOGO")
    pygame.display.set_icon(pygame.image.load("icon.png"))

    fonte = pygame.font.SysFont("monospace", 22)
    placar_fonte = pygame.font.SysFont("monospace", 42)

    bloco_matriz = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    desfazer_jogada = []

    main()
