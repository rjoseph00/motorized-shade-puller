"""
Driver.py library procured from Abe Hoffman

https://github.com/abehoffman

"""
from machine import I2C, Pin

from wsh1107 import SH1107_I2C
i2c = I2C(sda=Pin(23), scl=Pin(22))

class OLED(SH1107_I2C):
    def __init__(self):
        super().__init__(width=128, height=64, i2c=i2c)

    def clear(self):
        self.fill(0)

    def write_text(self, text: str) -> None:
        self.clear()
        if len(text) > 128:
            self.text("Too much text.", 0, 0, 1)

        else:
            lines = ["" for _ in range(8)]
            active_line = 0
            char = 0
            valid = True
            while char < len(text):
                if len(lines[active_line]) == 16 or text[char] == "\n":
                    active_line += 1

                if text[char] != "\n":
                    lines[active_line] += text[char]
                char += 1

                if active_line > 7:
                    valid = False
                    break

            if valid:
                for idx, line in enumerate(lines):
                    if line:
                        self.text(line, 0, idx*8, 1)
            else:
                self.text("Too many lines.", 0, 0, 1)

        self.show()
"""
    def qr(self):
        self.clear()

        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                self.fill_rect(i*2 + 33,j*2 + 1, 2, 2, col)
        self.show()
"""