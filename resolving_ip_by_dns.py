# encoding:utf-8

import dns.resolver
import pika


class ResolvingIp(object):
    def __init__(self, domain):
        self.domain = domain

    def get_a_record(self):
        A = dns.resolver.query(self.domain, 'A')
        for i in A.response.answer:
            for j in i.items:
                yield j.address


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ResolvingIp(body).get_a_record()


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()