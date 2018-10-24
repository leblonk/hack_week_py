import time

from neopixel import *

from config import *

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                          LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                          LED_STRIP)

strip.begin()
led_trigger = open('/sys/class/leds/led0/trigger', 'w')
led_trigger.write('gpio')

def test_main():
    while True:
        led = open('/sys/class/leds/led0/brightness', 'w')
        led.write('1')
        led.close()

        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(255, 0, 0))
        strip.show()

        time.sleep(1)
        led = open('/sys/class/leds/led0/brightness', 'w')
        led.write('0')
        led.close()

        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 255, 0))
        strip.show()

        time.sleep(1)
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 255))
        strip.show()

        time.sleep(1)
