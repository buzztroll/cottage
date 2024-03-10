import logging
import signal
import subprocess
import sys
import time

import RPi.GPIO as GPIO

import buzz_cottage.motion as buzzmo
import buzz_cottage.button as buzzbutt


class Cottage(object):

    def __init__(self, script_exe, motion_pin=25, button_pin=15):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(motion_pin, GPIO.IN)

        self.button_pin = button_pin
        self.motion_throttle = buzzmo.BuzzEventThrottle(self.motion_detected)
        self.script = script_exe
        self.button_mgr = buzzbutt.BuzzCottageButton()
        self.buzz_gpio = buzzmo.BuzzGPIODetector()
        self.buzz_gpio.add_handler(motion_pin, self.motion_throttle.moved)
        self.buzz_gpio.add_handler(button_pin, self.button_pressed)

    def button_pressed(self):
        self.button_mgr.button_pressed()
        while GPIO.input(self.button_pin) == GPIO.HIGH:
            time.sleep(0.01)
        self.motion_detected()

    def motion_detected(self):
        state = self.button_mgr.get_state()
        if state == buzzbutt.BuzzCottageButton.STATE_OFF:
            logging.debug("Motion detected but this is off")
            return
        try:
            subprocess.call(self.script, shell=True)
        except Exception as ex:
            logging.exception("failed to run")

    def run(self):
        try:
            self.buzz_gpio.start()
            signal.pause()
        except KeyboardInterrupt as ex:
            logging.exception("Ending")
            self.buzz_gpio.stop()
            logging.debug("Joining")
            self.buzz_gpio.join()
        finally:
            GPIO.cleanup()


def main():
    c = Cottage('/home/bresnaha/Dev/cottage/scripts/welcome.sh')
    c.run()
    return 0

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
