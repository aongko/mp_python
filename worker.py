import random
from time import sleep

import pika
import json

credentials = pika.PlainCredentials("aongko", "secret")
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=credentials))
channel = connection.channel()

queue_name = "something"
channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    something = json.loads(str(body.decode("utf-8")))
    print("Doing {}".format(something))
    sleep(random.uniform(2, 3))
    print("Done doing {}".format(something))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)


if __name__ == "__main__":
    channel.start_consuming()
