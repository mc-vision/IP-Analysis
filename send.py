#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.245.146.146', port=5672,
                              credentials=pika.PlainCredentials("hit", "hit")))

channel = connection.channel()

channel.queue_declare(queue='origin_ip')

channel.basic_publish(exchange='',
                      routing_key='origin_ip',
                      body='45.203.98.222')
print(" [x] Sent 'Hello World!'")
connection.close()
