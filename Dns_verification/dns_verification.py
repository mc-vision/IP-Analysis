# encoding: utf-8
"""
说明：这个代码的功能从origin_ip消息管道中接收经过反向解析后的ip和域名，并将域名进行dns探测，判断一致性，将合格后的数据放入
malicious_detected消息管道中；

Attention：这是这个模块唯一需要运行的代码

Author @ wangjunxiong

"""

import pika
from gevent.pool import Pool
from gevent import monkey
import gevent
from resolving_ip_cname_by_dns import obtaining_domain_ip  # dns探测


class DNSVerification:
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
            print '[*] Receive (IP, [domains]). %s' % body
            self.gevent_pool(body.split('\n'))  # 将获得的数据放入协程池中
        except Exception as e:
            return e

    def rabbitmq_comsumer(self):
        self.channel.queue_declare(queue='dns_verification')
        self.channel.basic_consume(on_message_callback=self.callback, queue='dns_verification', auto_ack=True)
        print(' [*] Waiting for (IP, [domains]) from MQ.')
        self.channel.start_consuming()

    def gevent_pool(self, message_set):
        """
        :param message_set:
        :return: None
        将消息队列接收到的域名按照分块大小放入协程池中，下面是几个重要参数
        coroutine_num: 协程数
        split_num: 块儿大小，即每一组放入到协程池中的总ip数量
        """
        coroutine_num = 10
        p = Pool(coroutine_num)
        split_num = 4
        tasks = []
        for message_blocks in range(0, len(message_set), split_num):
            messages = message_set[message_blocks:message_blocks + split_num]
            for message in messages:
                tasks.append(p.spawn(obtaining_domain_ip, message))
            gevent.joinall(tasks)

        # for task in tasks:
        #     print task.value  # 返回的数据结构为tuple类型 (ip, [domains])
        #     self.channel.queue_declare(queue='dns_verification')
        #     self.channel.basic_publish(exchange='',
        #                                routing_key='dns_verification',
        #                                body=task.value)
        #     print 'send success'


if __name__ == '__main__':
    DNSVerification().rabbitmq_comsumer()