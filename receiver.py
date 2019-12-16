# encoding:utf-8

import dns.resolver
import pika
import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import time
import random

success = 0
failed = 0
nameservers = ['1.2.4.8', '219.141.140.10', '219.141.136.10', '202.106.46.151', '202.106.196.115', '202.106.0.20',
               '202.106.195.68', '210.22.84.3', '210.22.70.3', '202.96.209.133', '116.228.111.118', '202.96.209.5'
               '180.168.255.118']


class RabbitMQ:
    def __init__(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='120.24.170.233',
                                          credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
            self.channel = connection.channel()

            self.channel.queue_declare(queue='hello')
        except Exception as e:
            print e

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        yield body

    def consume(self):
        self.channel.basic_consume(
            queue='hello', on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')

        self.channel.start_consuming()


RAMQ = RabbitMQ()


def get_a_record(domain):
    global success, failed
    dns.resolver.Resolver(configure=False)
    dns.resolver.Resolver.nameservers = random.choice(nameservers)
    try:
        A = dns.resolver.query(domain, 'A')
        for i in A.response.answer:
            for j in i.items:
                print domain, j.address
        success += 1
        RAMQ.channel.basic_publish(exchange='', routing_key='rest', body=domain)
    except:
        print domain, 'failed'
        failed += 1


def gevent_pool(message):
    p = Pool(500)
    jobs = []
    domains = message.split('\n')
    split_num = 20000
    start = time.time()
    for n in range(0, len(domains), split_num):
        domain_set = domains[n:n+split_num]
        print domain_set
        for domain in domain_set:
            jobs.append(p.spawn(get_a_record, domain))
        gevent.joinall(jobs)
    print 'Total time:', time.time() - start
    print 'Success: ', str(success)
    print 'Failed: ', str(failed)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='120.24.170.233',
                                  credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
    channel = connection.channel()

    channel.queue_declare(queue='hello')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        gevent_pool(body)

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()