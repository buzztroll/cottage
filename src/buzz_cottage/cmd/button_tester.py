import logging
import RPi.GPIO as GPIO
import signal
import sys
import time

import buzz_cottage.motion as buzzmotion

g_index = 0


def main():
    button_pin = 15
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    light_pins = (18, 23, 24)
    for pin in light_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def _this_handler():
        global g_index
        print(f"Button was pushed! {g_index}")
        GPIO.output(light_pins[g_index], GPIO.LOW)
        g_index = g_index + 1
        if g_index >= len(light_pins):
            g_index = 0
        GPIO.output(light_pins[g_index], GPIO.HIGH)
        while GPIO.input(button_pin) == GPIO.HIGH:
            time.sleep(0.01)

    bm = buzzmotion.BuzzGPIODetector(0.1)
    try:
        bm.add_handler(button_pin, _this_handler)
        bm.start()
        signal.pause()
    except KeyboardInterrupt as ex:
        logging.exception("Ending")
        bm.stop()
        logging.debug("Joining")
        bm.join()
    finally:
        GPIO.cleanup()

    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
