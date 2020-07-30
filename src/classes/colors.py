class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (244, 67, 54)
        self.pink = (234, 30, 99)
        self.purple = (156, 39, 176)
        self.dark_purple = (103, 58, 183)
        self.blue = (33, 150, 243)
        self.aqua_green = (0, 150, 136)
        self.light_green = (139, 195, 74)
        self.green = (60, 175, 80)
        self.orange = (255, 152, 0)
        self.dark_orange = (255, 87, 34)
        self.brown = (121, 85, 72)

        self.colors_keys = {
            0: self.black,
            2: self.purple,
            4: self.dark_purple,
            8: self.green,
            16: self.aqua_green,
            32: self.light_green,
            64: self.pink,
            128: self.blue,
            256: self.dark_orange,
            512: self.orange,
            1024: self.pink,
            2038: self.brown
        }

    def get_color(self, i: int):
        return self.colors_keys[i]
