# encoding: utf-8

from tencent_detect import TencentManager
from baidu_detect import BaiduDefender
from Sanliuling_detect import Sanliuling
from Jinshan_detect import Jinshan
from macfree_detect import Macfree
from virustotal_detect import Virustotal

import pika
from gevent.pool import Pool
from gevent import monkey
# monkey.patch_all()
import gevent


class DetectTools:
    def __init__(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='10.245.146.146', port=5672,
                                          credentials=pika.PlainCredentials("hit", "hit")))
            self.channel = connection.channel()
        except Exception as err:
            print str(err)

    def callback(self, ch, method, properties, body):
        try:
            print ' [*] Receive message. %s' % body
            self.gevent_pool(body)  # 将获得的数据放入协程池中
        except Exception as e:
            return e

    def rabbitmq_comsumer(self):
        self.channel.queue_declare(queue='malicious_detection')
        self.channel.basic_consume(on_message_callback=self.callback, queue='malicious_detection', auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def gevent_pool(self, message_set):
        """
        :param message_set:
        :return: None
        将消息队列接收到的域名按照分块大小放入协程池中，下面是几个重要参数
        coroutine_num: 协程数
        split_num: 块儿大小，即每一组放入到协程池中的总ip数量
        """

        message_set = eval(message_set)
        domain = message_set[1]
        coroutine_num = 10
        p = Pool(coroutine_num)
        split_num = 4
        tasks = []
        tasks.append(p.spawn(BaiduDefender().detect_domain, domain))
        gevent.joinall(tasks)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='10.245.146.146', port=5672,
                                      credentials=pika.PlainCredentials("hit", "hit")))
        for task in tasks:
            total_message = [message_set, task.value]
            print ' [*] All message. ',  total_message
            channel = connection.channel()
            channel.queue_declare(queue='detection_result')
            channel.basic_publish(exchange='',
                                  routing_key='detection_result',
                                  body=str(total_message))
            print(" [x] Sent to * MQ - detection_result * Success!"), total_message
            # print type(message_set), type(task.value)
        # for message_blocks in range(0, len(message_set), split_num):
        #     messages = message_set[message_blocks:message_blocks + split_num]
        #     for message in messages:
        #         tasks.append(p.spawn(BaiduDefender().detect_domain, domain))
        #     gevent.joinall(tasks)
        #
        # for task in tasks:
        #     print task.value
        # for task in tasks:
        #     print task.value  # 返回的数据结构为tuple类型 (ip, [domains])
        #     self.channel.queue_declare(queue='dns_verification')
        #     self.channel.basic_publish(exchange='',
        #                                routing_key='dns_verification',
        #                                body=task.value)
        #     print 'send success'


if __name__ == '__main__':
    DetectTools().rabbitmq_comsumer()
