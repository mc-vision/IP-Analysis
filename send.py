import pika
from domains import domains
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='120.24.170.233', port=5672,
                              credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body=domains)
print(" [x] Sent %s" % domains)

connection.close()
