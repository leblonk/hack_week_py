from neopixel import *

SCREEN_X = 62
SCREEN_Y = 31
P_MFACTOR = 8  # Screen multiplication factor for preview

# Do not display preview screen (pygame)
NO_PREVIEW = True

# LED strip configuration:
LED_COUNT = SCREEN_X * SCREEN_Y
LED_PIN = 13
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 1  # set to '1' for GPIOs pins 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB

SWITCH = 3  # switch for test vs display
