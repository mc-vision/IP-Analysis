#!/usr/bin/env python
import pika
from ip import ips
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.245.146.146', port=5672,
                              credentials=pika.PlainCredentials("hit", "hit")))

channel = connection.channel()

channel.queue_declare(queue='origin_ip')

# for ip in ips.split('\n'):
#     channel.basic_publish(exchange='',
#                           routing_key='origin_ip',
#                           body=ip)
#     print(" [x] Sent %s " % ip, 'Success!')

# single domain test

domains = ["204.11.56.48"]
for domain in domains:
    channel.basic_publish(exchange='',
                          routing_key='origin_ip',
                          body=domain)
    print(" [x] Sent %s " % domain, 'Success!')
connection.close()
