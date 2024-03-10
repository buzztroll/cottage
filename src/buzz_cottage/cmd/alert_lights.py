import logging
import sys

import buzz_cottage.lights as lights


def main():
    w = lights.AlertLights()
    try:
        w.start()
        w.join()
        w.off()
        logging.info("Done")
    except KeyboardInterrupt:
        logging.warning("User killed")
        w.off()
        raise


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
