import pygame
from flask import Flask, request, abort, make_response
from neopixel import *
from scipy import misc

from config import *
from utils import blink_onboard_led, reset_onboard_led

# Init preview screen
if not NO_PREVIEW:
    pygame.display.set_mode((SCREEN_X * P_MFACTOR, SCREEN_Y * P_MFACTOR))

# Init socketio and Flask
app = Flask(__name__)

reset_onboard_led()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()


@app.route('/frame/json', methods=['POST'])
def frame_json():
    data = request.get_json(force=True)
    if not data:
        abort(400)

    blink_onboard_led()

    update_screen(data)

    return make_response('', 200)


@app.route('/frame/image', methods=['POST'])
def frame_image():
    data = request.get_data()
    if not data:
        abort(400)

    # saving to a temp file because imread cannot read binary from memory
    tmp_file = open('/tmp/led_frame', 'wb')
    tmp_file.write(data)
    tmp_file.close()

    image_data = misc.imread('/tmp/led_frame')

    blink_onboard_led()

    update_screen(image_data)

    return make_response('', 200)


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


def get_rgb(data, (x, y)):
    try:
        (r, g, b) = data[y][x]
    except:
        r, g, b = 0, 0, 0
    return r, g, b


def set_pixel_color((x, y), (r, g, b)):
    if x & 1 == 1:
        i = (x + 1) * SCREEN_Y - y - 1
    else:
        i = x * SCREEN_Y + y
    strip.setPixelColor(i, Color(r, g, b))


if __name__ == '__main__':
    app.run()
