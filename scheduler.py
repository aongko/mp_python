import pika
import json

# establish a connection with RabbitMQ server
credentials = pika.PlainCredentials("aongko", "secret")
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=credentials))
channel = connection.channel()

# make sure the recipient queue exists
queue_name = "something"
channel.queue_declare(queue=queue_name)
# ready to send a message

if __name__ == "__main__":
    for i in range(1000):
        print(i)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=json.dumps(i))
        print("Sent {}".format(i))

connection.close()
