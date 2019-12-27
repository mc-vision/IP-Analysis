# encoding:utf-8
import pika

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='10.245.146.146', port=5672,
                                  credentials=pika.PlainCredentials("hit", "hit")))
channel = connection.channel()

channel.queue_declare(queue='detection_result')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(on_message_callback=callback, queue='detection_result', auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
