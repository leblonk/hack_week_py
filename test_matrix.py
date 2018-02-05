import time

import pygame
from neopixel import *

from config import *
from utils import get_serial_pixel

DELAY_SECONDS = 0.1

# Init preview screen
if not NO_PREVIEW:
    pygame.display.set_mode((SCREEN_X * P_MFACTOR, SCREEN_Y * P_MFACTOR))

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()


def update_screen(data):
    for y in range(SCREEN_Y):
        for x in range(SCREEN_X):
            (r, g, b) = get_rgb(data, (x, y))
            set_pixel_color((x, y), (r, g, b))
            if not NO_PREVIEW:
                pygame.display.get_surface().set_at((x * P_MFACTOR, y * P_MFACTOR), (r, g, b))
    strip.show()
    if not NO_PREVIEW:
        pygame.display.flip()
        pygame.event.get()


def set_pixel_color((x, y), (r, g, b)):
    i = get_serial_pixel(x, y, SCREEN_Y)
    strip.setPixelColor(i, Color(r, g, b))


def get_rgb(data, (x, y)):
    try:
        (r, g, b) = data[y][x]
    except:
        r, g, b = 0, 0, 0
    return r, g, b


if __name__ == '__main__':
    for x in range(SCREEN_X):
        for y in range(SCREEN_Y):
            data = [[0] * SCREEN_X for i in range(SCREEN_Y)]
            try:
                data[y][x] = (255, 255, 255)
                update_screen(data)
            except:
                print("failed on pixel", x, y)
            time.sleep(0.5)
