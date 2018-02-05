import netifaces as ni
import time


def reset_onboard_led():
    # Disable green onboard LED to indicate progress in headless run
    led_trigger = open('/sys/class/leds/led0/trigger', 'w')
    led_trigger.write('gpio')
    led_trigger.close()


def blink_onboard_led():
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('1')
    led.close()
    time.sleep(0.05)
    led = open('/sys/class/leds/led0/brightness', 'w')
    led.write('0')
    led.close()


def get_serial_pixel(x, y, size_y):
    if x & 1 == 1:
        i = (x + 1) * size_y - y - 1
    else:
        i = x * size_y + y
    return i


def get_ip_address(ifname):
    ni.ifaddresses(ifname)
    return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
