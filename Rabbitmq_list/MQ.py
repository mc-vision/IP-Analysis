# encoding: utf-8
import pika
HOST = '10.245.146.146'
PORT = 5672
ORIGIN_IP = 'origin_ip'
DNS_VERIFICATION = 'dns_verifiation'
DETECTION_RESULT = 'detection_result'
MALICIOUS_DETECTION = 'malicious_detection'


class rabbitmq:
    def __init__(self):

        try:
            self.__connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=HOST, port=PORT,
                                          credentials=pika.PlainCredentials("hit", "hit")))
        except Exception as e:
            raise e
            pass

    def publish(self, queue, data):
        channel = self.__connection.channel()
        try:
            channel.queue_declare(queue=queue)
            channel.basic_publish(exchange='',
                                  routing_key=queue,
                                  body=str(data))
        except Exception as e:
            return e


if __name__ == '__main__':
    pass
