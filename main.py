import time

import pygame

from config import *
from slideshow import slideshow_main
from test import test_main
from utils import get_ip_address, blink_onboard_led, reset_onboard_led, get_serial_pixel, read_test_switch

reset_onboard_led()

print('start', flush=True)
switch = open('/sys/class/gpio/gpio4/value', 'r')
statusStr = switch.read().strip()
print('status' + statusStr, flush=True)

if __name__ == '__main__':
    if read_test_switch():
        test_main()
    else:
        slideshow_main();
