import time

import pygame
import logging
import sys

from config import *
from slideshow import slideshow_main
from test import test_main
from utils import get_ip_address, blink_onboard_led, reset_onboard_led, get_serial_pixel, read_test_switch

print('starting...')
reset_onboard_led()

if __name__ == '__main__':
    if read_test_switch():
        print('running test pattern')
        test_main()
    else:
        print('running slideshow')
        slideshow_main();
