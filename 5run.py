import logging
import queue
import random
import signal
import threading
import time
import uuid

log_format = '%(asctime)s-%(levelname)s-%(processName)s - %(threadName)s - %(message)s'
logging.basicConfig(level="DEBUG", format=log_format)

STOP = uuid.uuid4()
FINISH = uuid.uuid4()


class Worker(threading.Thread):
    def __init__(self, name, input_queue, output_queue, callback):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self._callback = callback

        self._stop_event = threading.Event()

        super(Worker, self).__init__(
            name=name, target=self.process_queue,
            args=(input_queue, output_queue, callback,)
        )

    def process_queue(self, input_queue, output_queue, callback):
        while True:
            if self.stopped:
                logging.info("Current worker is stopping.")
                break

            try:
                item = input_queue.get(timeout=2)
                if item == FINISH:
                    logging.info("Finishing worker")
                    input_queue.task_done()
                    break
            except queue.Empty:
                logging.info("Waiting for item in queue...")
                time.sleep(1)
                continue

            try:
                result = callback(item)
                output_queue.put(result)
                input_queue.task_done()
            except Exception as e:
                logging.exception("Got exception: {}".format(str(e)))
                raise

        logging.info("End of worker")

    @property
    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()


class Job:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()

        self._workers = []

        self._stop_event = threading.Event()

    @property
    def stopped(self):
        return self._stop_event.is_set()

    def _prepare_workers(self, max_workers=4):
        for i in range(max_workers):
            worker = Worker("Worker-{}".format(i + 1),
                            self.input_queue,
                            self.output_queue,
                            self.process_item)
            worker.setDaemon(True)
            worker.start()
            self._workers.append(worker)

    @staticmethod
    def process_item(item):
        logging.info("Doing {}".format(item))
        time.sleep(random.uniform(1, 3))
        logging.info("Done doing {}".format(item))
        return item * item

    def start(self):
        self._prepare_workers()

        logging.info("Scheduling items")
        for i in range(10):
            self.input_queue.put(i)
            time.sleep(0.1)
        logging.info("Done scheduling items")

        for _ in self._workers:
            self.input_queue.put(FINISH)

        while True:
            if self.stopped:
                logging.info("Current job is being stopped.")
                break

            if not self.input_queue.empty():
                logging.info("Waiting for items to be completed")
                time.sleep(0.5)
            else:
                logging.info("Input queue is now empty")
                self.input_queue.join()
                break

        for worker in self._workers:
            if worker.is_alive():
                logging.info("Stopping worker {}".format(worker.name))
                worker.stop()

        while self._workers:
            worker = self._workers.pop()
            logging.info("Joining worker {}".format(worker.name))
            worker.join(timeout=2)
            logging.info("Worker {} joined".format(worker.name))

        logging.info("Getting results...")
        results = []
        while not self.output_queue.empty():
            results.append(self.output_queue.get())
            self.output_queue.task_done()
        logging.info("Results: {}".format(results))

        logging.info("Job done")

    def stop(self):
        self._stop_event.set()


def main():
    job = Job()

    def signal_handler(_, __):
        job.stop()

    signal.signal(signal.SIGINT, signal_handler)

    job.start()


if __name__ == "__main__":
    main()
