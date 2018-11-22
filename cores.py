class Cores:
    def __init__(self):
        self.branco = (255, 255, 255)
        self.preto = (0, 0, 0)
        self.vermelho = (244, 67, 54)
        self.rosa = (234, 30, 99)
        self.roxo = (156, 39, 176)
        self.roxo_escuro = (103, 58, 183)
        self.azul = (33, 150, 243)
        self.verde_agua = (0, 150, 136)
        self.verde_claro = (139, 195, 74)
        self.verde = (60, 175, 80)
        self.laranja = (255, 152, 0)
        self.laranja_escuro = (255, 87, 34)
        self.marrom = (121, 85, 72)

        self.dicionario_cores = {
            0: self.preto,
            2: self.roxo,
            4: self.roxo_escuro,
            8: self.verde,
            16: self.verde_agua,
            32: self.verde_claro,
            64: self.rosa,
            128: self.azul,
            256: self.laranja_escuro,
            512: self.laranja,
            1024: self.rosa,
            2038: self.marrom
        }

    def obter_cor(self, i: int):
        return self.dicionario_cores[i]