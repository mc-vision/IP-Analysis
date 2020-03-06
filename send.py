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
channel.basic_publish(exchange='',
                      routing_key='origin_ip',
                      body="39.106.165.57")
print(" [x] Sent %s " % "39.106.165.57", 'Success!')
connection.close()
