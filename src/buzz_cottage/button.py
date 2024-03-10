import logging
import RPi.GPIO as GPIO

class BuzzCottageButton(object):
    STATE_OFF = 0
    STATE_WELCOME = 1
    STATE_ALARM = 2

    def __init__(self, red_pin=23, green_pin=18, blue_pin=24):
        self.state = BuzzCottageButton.STATE_OFF
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.light_pins = (self.green_pin, self.blue_pin, self.red_pin)
        for pin in self.light_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.light_pins[self.state], GPIO.HIGH)

    def button_pressed(self):
        GPIO.output(self.light_pins[self.state], GPIO.LOW)
        self.state = self.state + 1
        if self.state > BuzzCottageButton.STATE_ALARM:
            self.state = BuzzCottageButton.STATE_OFF
        GPIO.output(self.light_pins[self.state], GPIO.HIGH)

    def get_state(self):
        return self.state
