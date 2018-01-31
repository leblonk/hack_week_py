import time
import os

from neopixel import *

NUM_PIXELS = 1000
LED_PIN = 13
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 1  # set to '1' for GPIOs pins 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB

strip = Adafruit_NeoPixel(NUM_PIXELS, LED_PIN, LED_FREQ_HZ, LED_DMA,
                          LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                          ws.WS2811_STRIP_RGB)

strip.begin()
led_trigger = open('/sys/class/leds/led0/trigger', 'w')
led_trigger.write('gpio')

while True:
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('1')
    led.close()

    for i in range(NUM_PIXELS):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()

    time.sleep(1)
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('0')
    led.close()

    for i in range(NUM_PIXELS):
        strip.setPixelColor(i, Color(0, 255, 0))
    strip.show()

    time.sleep(1)
    for i in range(NUM_PIXELS):
        strip.setPixelColor(i, Color(0, 0, 255))
    strip.show()

    time.sleep(1)