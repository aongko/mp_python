import logging
import signal
import threading

import time

log_format = '%(asctime)s-%(levelname)s-%(processName)s - %(threadName)s - %(message)s'

logging.basicConfig(format=log_format, level="DEBUG")


class StoppableThread(threading.Thread):
    def __init__(self, name):
        super(StoppableThread, self).__init__(name=name,
                                              target=self.process)

        self._stop_event = threading.Event()

    @property
    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def process(self):
        for i in range(10):
            if self.stopped:
                logging.info("Got stop signal.")
                break
            logging.info("i: {}".format(i))
            time.sleep(1)


def main():
    logging.info("Starting")
    thread = StoppableThread(
        name="my stoppable thread"
    )
    thread.setDaemon(True)
    thread.start()

    def signal_handler(signum, frame):
        thread.stop()

    signal.signal(signal.SIGINT, signal_handler)

    logging.info("Waiting for thread...")
    thread.join()

    logging.info("Done")


if __name__ == "__main__":
    main()
