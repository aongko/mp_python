import logging
import queue
import random
import threading
import time
import uuid

log_format = '%(asctime)s-%(levelname)s-%(processName)s - %(threadName)s - %(message)s'

logging.basicConfig(format=log_format, level="DEBUG")

FINISH = uuid.uuid4()


def do(something):
    logging.info("doing {}".format(something))
    time.sleep(random.uniform(1, 3))
    logging.info("done doing {}".format(something))


def process_queue(input_queue):
    while True:
        logging.info("Getting item...")
        item = input_queue.get()
        if item == FINISH:
            logging.info("Got FINISH signal")
            input_queue.task_done()
            break
        logging.info("Got item in queue: {}".format(item))
        do(item)
        input_queue.task_done()


def main():
    myqueue = queue.Queue()

    threads = []

    max_workers = 2
    logging.info("Starting threads")
    for i in range(max_workers):
        thread = threading.Thread(
            name="Thread #{}".format(i + 1),
            target=process_queue,
            args=(myqueue,)
        )
        thread.setDaemon(True)
        thread.start()

    logging.info("Start putting item to queue")
    for i in range(10):
        myqueue.put(i)
    logging.info("Done putting item to queue")

    for i in range(max_workers):
        myqueue.put(FINISH)

    logging.info("Waiting...")
    myqueue.join()
    logging.info("All Done!")

    logging.info("Joining threads")
    for thread in threads:
        thread.join()

    logging.info("Done")


if __name__ == "__main__":
    main()
