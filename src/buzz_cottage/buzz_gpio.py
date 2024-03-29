import logging
import threading
import time

import RPi.GPIO as GPIO


_g_logger = logging.getLogger(__file__)


class _BuzzGPIOHandler(threading.Thread):
    def __init__(self, pin, cb, cb_kwargs=None):
        super().__init__()
        self.cb = cb
        if cb_kwargs is None:
            cb_kwargs = {}
        self.cb_kwargs = cb_kwargs
        self.running = False
        self._done = False
        self._cond = threading.Condition()
        self._fire = False
        self._pin = pin

    def run(self):
        fire = False
        while not self._done:
            with self._cond:
                self.running = False
                while not self._fire and not self._done:
                    self._cond.wait()
                self.running = True
                fire = self._fire
                self._fire = False
            if fire:
                try:
                    _g_logger.debug(f"Running the handler for pin {self._pin}")
                    self.cb(**self.cb_kwargs)
                    while GPIO.input(self._pin) == GPIO.HIGH:
                        time.sleep(0.01)
                except Exception as ex:
                    _g_logger.exception("handler exception")

    def fire_cb(self):
        _g_logger.debug(f"fire_cb for pin {self._pin} enter")
        try:
            with self._cond:
                if self.running:
                    _g_logger.debug(f"Handler for pin {self._pin} is already running")
                    return
                self._fire = True
                self._cond.notifyAll()
        finally:
            _g_logger.debug(f"fire_cb for pin {self._pin} exit")

    def stop(self):
        with self._cond:
            self._done = True
            self._fire = False
            self._cond.notify()


class BuzzGPIODetector(threading.Thread):
    def __init__(self, frequency=0.1):
        super().__init__()
        self._handler_table = {}
        self._done = False
        self._frequency = frequency
        self._cond = threading.Condition()

    def add_handler(self, pin, cb, cb_kwargs=None):
        with self._cond:
            _handler = _BuzzGPIOHandler(pin, cb, cb_kwargs=cb_kwargs)
            self._handler_table[pin] = _handler
            _handler.start()

    def force_handler(self, pin):
        _g_logger.info(f"Force the handler for pin {pin}")
        self._handler_table[pin].fire_cb()

    def stop(self):
        with self._cond:
            for pin in self._handler_table:
                _g_logger.info(f"Stopping pin {pin}")
                self._handler_table[pin].stop()
            self._done = True
            self._cond.notify()

    def run(self):
        with self._cond:
            while not self._done:
                for pin in self._handler_table:
                    if GPIO.input(pin):
                        _g_logger.debug(f"Pin {pin} is high")
                        self._handler_table[pin].fire_cb()
                self._cond.wait(self._frequency)

    def join(self):
        for pin in self._handler_table:
            _g_logger.debug(f"Waiting for pin {pin} thread to finish")
            self._handler_table[pin].join()
            _g_logger.debug(f"Pin {pin} thread finished")
        _g_logger.info("Waiting for BuzzGPIODetector thread to finish")
        super().join()
