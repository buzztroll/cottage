import logging
import signal
import subprocess
import sys
import time

import RPi.GPIO as GPIO

import buzz_cottage.motion as buzzmo
import buzz_cottage.buzz_gpio as buzz_gpio
import buzz_cottage.button as buzzbutt


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_g_logger = logging.getLogger(__file__)


class Cottage(object):

    def __init__(self, welcome_script, alert_script, motion_pin=25, button_pin=15):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.cleanup()
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(motion_pin, GPIO.IN)

        time.sleep(2)

        self.button_pin = button_pin
        self.motion_pin = motion_pin
        self.motion_throttle = buzzmo.BuzzEventThrottle(self.motion_detected, pace=60)
        self.welcome_script = welcome_script
        self.alert_script = alert_script
        self.button_mgr = buzzbutt.BuzzCottageButton()
        self.buzz_gpio = buzz_gpio.BuzzGPIODetector()
        self.buzz_gpio.add_handler(motion_pin, self.motion_throttle.moved)
        self.buzz_gpio.add_handler(button_pin, self.button_pressed)

    def button_pressed(self):
        _g_logger.info("Button pressed enter")
        self.button_mgr.button_pressed()
        while GPIO.input(self.button_pin) == GPIO.HIGH:
            time.sleep(0.01)
        self.motion_throttle.reset_fired()
        self.buzz_gpio.force_handler(self.motion_pin)
        _g_logger.info("Button pressed exit")

    def motion_detected(self):
        _g_logger.info("Motion detected enter")
        try:
            state = self.button_mgr.get_state()
            _g_logger.info(f"Motion detected state {state}")
            if state == buzzbutt.BuzzCottageButton.STATE_OFF:
                _g_logger.info("Motion detected but this is off")
                return
            if state == buzzbutt.BuzzCottageButton.STATE_ALARM:
                script = self.alert_script
            else:
                script = self.welcome_script
            try:
                _g_logger.info(f"Motion detected running {script}")
                subprocess.call(script, shell=True)
                _g_logger.info(f"Motion detected done {script}")
            except Exception as ex:
                _g_logger.exception("failed to run")
            while GPIO.input(self.motion_pin) == GPIO.HIGH:
                time.sleep(0.01)
        finally:
            _g_logger.info("Motion detected exit")

    def run(self):
        try:
            self.buzz_gpio.start()
            signal.pause()
        except KeyboardInterrupt as ex:
            _g_logger.exception("Ending")
            self.buzz_gpio.stop()
            _g_logger.info("Joining")
            self.buzz_gpio.join()
        finally:
            _g_logger.info("Clean up")
            GPIO.cleanup()


def main():
    c = Cottage('/home/bresnaha/Dev/cottage/scripts/welcome.sh', '/home/bresnaha/Dev/cottage/scripts/intruder.sh')
    c.run()
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
