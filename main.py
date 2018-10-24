import time

import pygame
import logging
import sys

from config import *
from slideshow import slideshow_main
from test import test_main
from utils import get_ip_address, blink_onboard_led, reset_onboard_led, get_serial_pixel, read_test_switch

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)

root.addHandler(ch)

logging.error('error')
reset_onboard_led()

print('start\n')
switch = open('/sys/class/gpio/gpio4/value', 'r')
statusStr = switch.read().strip()
print('status' + statusStr + '\n')

# if __name__ == '__main__':
#     if read_test_switch():
#         test_main()
#     else:
#         slideshow_main();
