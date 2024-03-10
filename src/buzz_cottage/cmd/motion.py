import logging
import subprocess
import sys

import buzz_cottage.motion as motion


def _moved(exefile):
    logging.info(f"running {exefile}")
    try:
        subprocess.call(exefile, shell=True)
    except Exception as ex:
        logging.exception("failed to run")


def main():
    run_file = sys.argv[1]
    bm = motion.BuzzMotion(_moved, args={'exefile': run_file})
    bm.start()
    bm.join()
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
