# I2C OLED 7-segment emulator library for the micro:bit
from microbit import i2c, sleep

# LCD Control constants
ADDR = 0x3C
# Holds the segments on in each of the four digits
display = []  
# Segments to set to on for each of the 10 digits. 10 represents empty.
digits = b'\xFC\x60\xDA\xF2\x66\xB6\xBE\xE0\xFE\xF6\x00' 
# Position of each of the 8 segments
rects = [[5, 20, 0, 0],
         [21, 25, 0, 3],
         [21, 25, 4, 6],
         [5, 20, 6, 6],
         [0, 4, 4, 6],
         [0, 4, 0, 3],
         [5, 20, 3, 3],
         [27, 32, 6, 6]
         ]
seg_len = [16, 21, 16, 17, 16, 21, 17, 7]
segments = []
with open('segments.bin', 'rb') as f:
    for i in seg_len:
        segments.append(f.read(i))
dispZeros = 1


def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))


def initialize(showDots=0, showZeros=1):
    global dispZeros, display
    cmd = [
        [0xAE],                    # DISPLAYOFF
        [0xA4],           # DISPLAYALLON_RESUME
        [0xD5, 0xF0],            # SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],                  # SETMULTIPLEX
        [0xD3, 0x00],              # SETDISPLAYOFFSET
        [0 | 0x0],                   # SETSTARTLINE
        [0x8D,  0x14],                    # CHARGEPUMP
        [0x20,  0x00],  # MEMORYMODE horizontal
        [0x21,  0, 127],  # COLUMNADDR
        [0x22,  0, 63],   # PAGEADDR
        [0xa0 | 0x1],  # SEGREMAP
        [0xc8],   # COMSCANDEC
        [0xDA,  0x12],                    # SETCOMPINS
        [0x81,  0xCF],                   # SETCONTRAST
        [0xd9,  0xF1],                  # SETPRECHARGE
        [0xDB,  0x40],                 # SETVCOMDETECT
        [0xA6],                 # NORMALDISPLAY
        [0xd6, 0],  # zoom off

    ]
    for c in cmd:
        command(c)
    clear_oled()
    display = [0, 0, 0, 0]
    dispZeros = showZeros
    disp_number(0)
    if showDots == 1:
        for i in range(0, 3, 2):
            set_rect([61, 66, 2 + i, 2 + i])
            i2c.write(ADDR, segments[7])
    command([0xaf])  # SSD1306_DISPLAYON


def set_rect(rect):
    command([0x21, rect[0], rect[1]])
    command([0x22, rect[2], rect[3]])


def clear_oled():
    set_rect([0, 127, 0, 7])
    screen = bytearray(33)
    screen[0] = 0x40
    for i in range(0, 32):
        i2c.write(ADDR, screen)


def disp_number(n):
    global dispZeros
    for j in range(0, 4):
        v = (n // 10**j) % 10
        if v == 0 and dispZeros == 0:
            set_digit(j, 10, 0)
        else:
            set_digit(j, v, 0)


def set_digit(dig, val, dec):
    global digits, display, segments

    c, d = display[dig], digits[val] + dec
    if c != d:
        b1, b2 = c & ~ d, ~c & d
        for i in range(0, 8):
            r1, r2 = b1 >> (7 - i) & 1, b2 >> (7 - i) & 1
            if r2 or r1:
                offset, rect = 34 * (3 - dig), rects[i]
                set_rect([rect[0]+offset, rect[1]+offset, rect[2], rect[3]])
                if r2:  # d and not c:
                    i2c.write(ADDR, segments[i])
                elif r1:  # not d and c:
                    i2c.write(ADDR, b'\x40' + bytearray(seg_len[i] - 1))
        display[dig] = d

def blink(time=1000):
    for c in ([0xae], [0xaf]):
        command(c)
        sleep(time/4)
