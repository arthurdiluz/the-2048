import pygame, sys
from pygame.locals import *
from tabuleiro import *


def main(esta_carregado=False):

    if not esta_carregado:
        tabuleiro.posicionar_bloco()
        tabuleiro.posicionar_bloco()

    tabuleiro.exibir_matriz()

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()

            if tabuleiro.checar_ir():
                if evento.type == KEYDOWN:
                    if tabuleiro.setas(evento.key):
                        rotacoes = tabuleiro.obter_rotacao(evento.key)

                        tabuleiro.add_desfazer()

                        for i in range(rotacoes):
                            tabuleiro.rotacionar_matriz()

                        if tabuleiro.pode_mover():
                            tabuleiro.mover_bloco()
                            tabuleiro.mesclar_blocos()
                            tabuleiro.posicionar_bloco()

                        for j in range((4 - rotacoes) % 4):
                            tabuleiro.rotacionar_matriz()

                        tabuleiro.exibir_matriz()
            else:
                tabuleiro.exibir_gameover()

            if evento.type == KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if evento.key == pygame.K_r:
                    tabuleiro.reiniciar()
                    main()

                if 50 < evento.key < 56:
                    tabuleiro.reiniciar()

                elif evento.key == pygame.K_u:
                    tabuleiro.desfazer()

        pygame.display.update()


if __name__ == '__main__':

    pygame.init()

    pygame.display.set_caption("O JOGO")
    pygame.display.set_icon(pygame.image.load("icon.png"))

    tabuleiro = Matriz(
        pygame.display.set_mode((400, 500), 0, 32),
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [],
        pygame.font.SysFont("monospace", 22),
        pygame.font.SysFont("monospace", 42)
    )

    main()
