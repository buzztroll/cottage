import logging
import signal
import subprocess
import sys
import time

import RPi.GPIO as GPIO

import buzz_cottage.motion as buzzmo
import buzz_cottage.buzz_gpio as buzz_gpio
import buzz_cottage.button as buzzbutt


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
_g_logger = logging.getLogger(__file__)


class Cottage(object):

    def __init__(self, welcome_script, alert_script, motion_pin=25, button_pin=15):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(motion_pin, GPIO.IN)

        self.button_pin = button_pin
        self.motion_throttle = buzzmo.BuzzEventThrottle(self.motion_detected, pace=60*10)
        self.welcome_script = welcome_script
        self.alert_script = alert_script
        self.button_mgr = buzzbutt.BuzzCottageButton()
        self.buzz_gpio = buzz_gpio.BuzzGPIODetector()
        self.buzz_gpio.add_handler(motion_pin, self.motion_throttle.moved)
        self.buzz_gpio.add_handler(button_pin, self.button_pressed)

    def button_pressed(self):
        self.button_mgr.button_pressed()
        while GPIO.input(self.button_pin) == GPIO.HIGH:
            time.sleep(0.01)
        self.motion_detected()
        self.motion_throttle.update_fired()

    def motion_detected(self):
        state = self.button_mgr.get_state()
        if state == buzzbutt.BuzzCottageButton.STATE_OFF:
            _g_logger.debug("Motion detected but this is off")
            return
        if state == buzzbutt.BuzzCottageButton.STATE_ALARM:
            script = self.alert_script
        else:
            script = self.welcome_script
        try:
            subprocess.call(script, shell=True)
        except Exception as ex:
            _g_logger.exception("failed to run")

    def run(self):
        try:
            self.buzz_gpio.start()
            signal.pause()
        except KeyboardInterrupt as ex:
            _g_logger.exception("Ending")
            self.buzz_gpio.stop()
            _g_logger.debug("Joining")
            self.buzz_gpio.join()
        finally:
            GPIO.cleanup()


def main():
    c = Cottage('/home/bresnaha/Dev/cottage/scripts/welcome.sh', '/home/bresnaha/Dev/cottage/scripts/intruder.sh')
    c.run()
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
