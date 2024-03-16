import logging
import sys

import buzz_cottage.lights as lights

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_g_logger = logging.getLogger(__file__)


def main():
    w = lights.AlertLights()
    try:
        w.start()
        w.join()
        w.off()
        _g_logger.info("Done")
    except KeyboardInterrupt:
        _g_logger.warning("User killed")
        w.off()
        raise


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
