import logging
import sys

import buzz_cottage.lights as lights

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
_g_logger = logging.getLogger(__file__)


def main():
    w = lights.WelcomeLights(166, 172, 255, steps=90, wait_time=0.05)
    try:
        w.start()
        w.join()
        w.off()
        _g_logger.info("end")
    except KeyboardInterrupt:
        _g_logger.warning("User killed")
        w.off()
        raise


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
