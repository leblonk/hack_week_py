import time

import pygame
from PIL import Image, ImageDraw
from google.cloud import storage
from neopixel import *
from scipy import misc

from config import *
from utils import get_ip_address, blink_onboard_led, reset_onboard_led, get_serial_pixel

DELAY_SECONDS = 0.1

# Init preview screen
if not NO_PREVIEW:
    pygame.display.set_mode((SCREEN_X * P_MFACTOR, SCREEN_Y * P_MFACTOR))

reset_onboard_led()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

client = storage.Client()
bucket = client.get_bucket("big-led-screen-data")


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


def display_ip():
    try:
        ip = get_ip_address('wlan0')
        print(ip)
        for addr in ip.split('.'):
            img = Image.new('RGB', (60, 30), color='black')
            d = ImageDraw.Draw(img)
            d.text((10, 10), addr, fill=(255, 255, 255))
            img.save('/tmp/ip.png')
            ip_image = misc.imread('/tmp/ip.png')
            update_screen(ip_image)
            time.sleep(1)
    except:
        print('error displaying ip')

def slideshow_main():
    display_ip()
    while True:
        # allowing only blobs - files need to be < 1MB
        for blob in bucket.list_blobs():
            print("Display " + str(blob))

            # saving to a temp file because imread cannot read binary from memory
            try:
                tmp_file = open('/tmp/led_blob', 'wb')
                blob.download_to_file(tmp_file)
                tmp_file.close()

                image_data = misc.imread('/tmp/led_blob')

                blink_onboard_led()

                update_screen(image_data)
            except:
                print("Error displaying blob")

            time.sleep(DELAY_SECONDS)
