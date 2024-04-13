import board
import logging
import sys
import time

import neopixel


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_g_logger = logging.getLogger(__file__)


def clear_lights(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()


def _pulse_one_light(light, percent=.2, up=False):
    degree = light * percent
    if up:
        light = light + degree
        if light > 255:
            light = 255
    else:
        light = light - degree
        if light < 0:
            light = 0
    return light


def pulse_lights(pixels, total=50, up=False):
    for i in range(total):
        current_color = pixels[i]
        r = _pulse_one_light(current_color[0], up=up)
        g = _pulse_one_light(current_color[1], up=up)
        b = _pulse_one_light(current_color[2], up=up)
        pixels[i] = (r, g, b)
    pixels.show()


def main():
    three_colors = [
        (0, 50, 0),
        (0, 150, 0),
        (0, 255, 0)
    ]

    pin = board.D21

    pixels = neopixel.NeoPixel(pin, 50, auto_write=False)
    clear_lights(pixels)

    c_ndx = 0
    for i in range(50):
        if c_ndx >= len(three_colors):
            c_ndx = 0
        pixels[i] = three_colors[c_ndx]
        pixels.show()
        time.sleep(0.1)

    time.sleep(5)

    up = False
    for i in range(20):
        pulse_lights(pixels, up=up)
        up = not up
        time.sleep(0.5)

    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)