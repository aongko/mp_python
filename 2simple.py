import logging
import threading

import time

log_format = '%(asctime)s-%(levelname)s-%(processName)s - %(threadName)s - %(message)s'

logging.basicConfig(format=log_format, level="DEBUG")


def process():
    for i in range(10):
        logging.info("i: {}".format(i))
        time.sleep(0.1)


def main():
    logging.info("Starting")
    thread = threading.Thread(
        name="my thread",
        target=process
    )
    thread.setDaemon(True)
    thread.start()

    for i in range(100, 110):
        logging.info("i: {}".format(i))
        time.sleep(0.1)

    logging.info("Waiting for thread")
    thread.join()

    logging.info("Done")


if __name__ == "__main__":
    main()
