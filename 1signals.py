# Playing with signals

import logging
import signal
import time

log_format = '%(asctime)s-%(levelname)s-%(processName)s - %(threadName)s - %(message)s'

logging.basicConfig(format=log_format, level="DEBUG")

should_stop = False


def main():
    logging.info("Starting")

    def signal_handler(signum, frame):
        if signum == signal.SIGINT:
            logging.info("Got SIGINT")
        else:
            logging.info("Got SIGTERM")

        global should_stop
        should_stop = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    i = 0
    while True:
        if should_stop:
            break

        logging.info("i: {}".format(i))
        time.sleep(1)
        i += 1


if __name__ == "__main__":
    main()
