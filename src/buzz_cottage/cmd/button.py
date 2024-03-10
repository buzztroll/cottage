import RPi.GPIO as GPIO
import time


button_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

light_pins = (18, 23, 24)
for pin in light_pins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

index = 0

try:
    while True: # Run forever
        if GPIO.input(button_pin) == GPIO.HIGH:
            print(f"Button was pushed! {index}")
            GPIO.output(light_pins[index], GPIO.LOW)
            index = index + 1
            if index >= len(light_pins):
                index = 0
            GPIO.output(light_pins[index], GPIO.HIGH)
            while GPIO.input(button_pin) == GPIO.HIGH:
                time.sleep(0.01)
        time.sleep(.05)
finally:
    GPIO.cleanup()