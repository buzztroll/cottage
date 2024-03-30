import logging
import time
import threading


_g_logger = logging.getLogger(__name__)


class BuzzEventThrottle(object):
    def __init__(self, callback, args=None, pace=60, inline=True):
        self._cb = callback
        self._pace = pace
        self._last_fired = 0
        self._lock = threading.Lock()
        self._cb_thread = None
        self._running = False
        self._inline = inline
        self._cb_args = args
        if args is None:
            self._cb_args = {}

    def moved(self):
        now = time.time()
        fire = False
        self._lock.acquire()
        try:
            if now - self._last_fired < self._pace:
                _g_logger.debug("The event window is still open. Ignoring")
                return
            if self._running:
                _g_logger.info("The event handler is already running")
            self._running = True
            try:
                if self._inline:
                    fire = True
                else:
                    self._cb_thread = threading.Thread(target=self._fire_cb)
                    self._cb_thread.start()
            except:
                self._running = False
                raise
        finally:
            self._lock.release()
        if fire:
            self._fire_cb()

    def reset_fired(self):
        self._last_fired = 0

    def mark_fired(self):
        self._last_fired = time.time()

    def _fire_cb(self):
        _g_logger.debug("Running the throttled handler")
        self._last_fired = time.time()
        try:
            self._cb(**self._cb_args)
        finally:
            self._lock.acquire()
            try:
                self._running = False
            finally:
                self._lock.release()
