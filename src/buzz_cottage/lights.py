import board
import logging
import math
import neopixel
import time
import threading


_g_logger = logging.getLogger(__file__)


class FaderLight(object):
    def __init__(self, target_color, steps):
        self.target = target_color
        self.current = 0.0
        self.step = target_color / steps

    def fade_up(self):
        self.current = self.current + self.step
        if self.current > 255.0:
            self.current = 255.0
        return math.ceil(self.current)

    def fade_down(self):
        self.current = self.current - self.step
        if self.current < 0.0:
            self.current = 0.0
        return math.ceil(self.current)


class WelcomeLights(threading.Thread):
    def __init__(self,
                 target_red,
                 target_green,
                 target_blue,
                 light_count=50,
                 steps=120,
                 wait_time=0.1,
                 pin=board.D21):
        super().__init__()
        self.light_count = light_count
        self.pixels = neopixel.NeoPixel(pin, light_count, auto_write=True)
        self.red = FaderLight(target_red, steps)
        self.green = FaderLight(target_green, steps)
        self.blue = FaderLight(target_blue, steps)
        self.steps = steps
        self.wait_time = wait_time

    def _fade_on(self):
        for i in range(self.steps+2):
            red = self.red.fade_up()
            green = self.green.fade_up()
            blue = self.blue.fade_up()
            _g_logger.debug(f"{red}, {green}, {blue}")
            self.pixels.fill((red, green, blue))
            self.pixels.show()
            time.sleep(self.wait_time)

    def _fade_off(self):
        for i in range(self.steps+2):
            red = self.red.fade_down()
            green = self.green.fade_down()
            blue = self.blue.fade_down()
            _g_logger.debug(f"{red}, {green}, {blue}")
            self.pixels.fill((red, green, blue))
            self.pixels.show()
            time.sleep(self.wait_time)

    def run(self):
        try:
            self.off()
            self._fade_on()
            self._fade_off()
            self.off()
            _g_logger.info("final")
        except KeyboardInterrupt:
            _g_logger.warning("Ending lights!")
            self.off()

    def off(self):
        _g_logger.info("off")
        self.pixels.fill((0, 0, 0))
        self.pixels.show()


class AlertLights(threading.Thread):
    def __init__(self,
                 light_count=50,
                 steps=40,
                 wait_time=0.01,
                 pin=board.D21):
        super().__init__()
        self.light_count = light_count
        self.pixels = neopixel.NeoPixel(pin, light_count, auto_write=True)
        self.red = FaderLight(255, steps)
        self.steps = steps
        self.wait_time = wait_time

    def _fade_on(self):
        for i in range(self.steps+2):
            red = self.red.fade_up()
            self.pixels.fill((red, 0, 0))
            self.pixels.show()
            time.sleep(self.wait_time)

    def _fade_off(self):
        for i in range(self.steps+2):
            red = self.red.fade_down()
            self.pixels.fill((red, 0, 0))
            self.pixels.show()
            time.sleep(self.wait_time)

    def run(self):
        try:
            self.off()
            for i in range(10):
                self._fade_on()
                self._fade_off()
            self.off()
            _g_logger.info("final")
        except KeyboardInterrupt:
            _g_logger.warning("Ending lights!")
            self.off()

    def off(self):
        _g_logger.info("off")
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
