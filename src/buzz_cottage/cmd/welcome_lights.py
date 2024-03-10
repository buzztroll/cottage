import logging
import sys

import buzz_cottage.lights as lights


def main():
    w = lights.WelcomeLights(166, 172, 255, steps=90, wait_time=0.05)
    try:
        w.start()
        w.join()
        w.off()
        logging.info("end")
    except KeyboardInterrupt:
        logging.warning("User killed")
        w.off()
        raise


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
