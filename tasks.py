import random
from time import sleep

from celery import Celery

app = Celery("tasks",
             broker="pyamqp://aongko:secret@localhost/",
             backend="rpc://")


@app.task
def do(something):
    print("Doing {}".format(something))
    sleep(random.uniform(2, 3))
    print("Done doing {}".format(something))


if __name__ == "__main__":
    app.start()
