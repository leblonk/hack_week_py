import time

import eventlet.wsgi
import pygame
import socketio
from flask import Flask
from neopixel import *

SCREEN_X = 62
SCREEN_Y = 31
PORT = 5432
P_MFACTOR = 8  # Screen multiplication factor for preview

# LED strip configuration:
LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0  # set to '1' for GPIOs pins 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB

# Init preview screen
pygame.display.set_mode((SCREEN_X * P_MFACTOR, SCREEN_Y * P_MFACTOR))

# Init socketio and Flask
sio = socketio.Server()
app = Flask(__name__)

# Disabling green onboard LED to indicate progress in headless run
led_trigger = open('/sys/class/leds/led0/trigger', 'w')
led_trigger.write('gpio')
led_trigger.close()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()


@sio.on('/frame')
def message(sid, data):
    if not data:
        return

    blink_onboard_led()

    for y in range(SCREEN_Y):
        for x in range(SCREEN_X):
            (r, g, b) = get_rgb(data, (x, y))
            set_pixel_color((x, y), (r, g, b))
            pygame.display.get_surface().set_at((x * P_MFACTOR, y * P_MFACTOR), (r, g, b))

    strip.show()
    pygame.display.flip()
    pygame.event.get()


def get_rgb(data, (x, y)):
    try:
        (r, g, b) = data[str(y) + ',' + str(x)]
    except:
        r, g, b = 0, 0, 0
    return r, g, b


def set_pixel_color((x, y), (r, g, b)):
    if x & 1 == 1:
        i = (x + 1) * SCREEN_Y - y - 1
    else:
        i = x * SCREEN_Y + y
    strip.setPixelColor(i, Color(r, g, b))


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


def blink_onboard_led():
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('1')
    led.close()
    time.sleep(0.05)
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('0')
    led.close()


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', PORT)), app)
