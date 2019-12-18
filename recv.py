# encoding:utf-8

import dns.resolver
import pika

with open('domains.txt', 'a+') as f:

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='120.24.170.233',
                                  credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
    channel = connection.channel()

    channel.queue_declare(queue='hello')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print >> f, body

    channel.basic_consume(
        queue='rest', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()