# encoding:utf-8

import dns.resolver
import pika


class ResolvingIp(object):
    def __init__(self, domain):
        self.domain = domain

    def get_a_record(self):
        try:
            A = dns.resolver.query(self.domain, 'A')
            for i in A.response.answer:
                for j in i.items:
                    print j.address
                    channel.basic_publish(exchange='', routing_key='rest', body=self.domain + ' ' + j.address)
        except:
            print self.domain, 'failed'


class RabbitMQ(object):
    def __init__(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='120.24.170.233',
                                          credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
            self.channel = connection.channel()

            self.channel.queue_declare(queue='hello')
        except Exception as e:
            print e

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        ResolvingIp(body).get_a_record()





channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
