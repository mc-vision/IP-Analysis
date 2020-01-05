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
# monkey.patch_all()
import gevent
# from resolving_ip_cname_by_dns import obtaining_domain_ip  # dns探测
from database import DB


class DNSVerification:
    def __init__(self):
        self.db = DB()
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='10.245.146.146', port=5672,
                                          credentials=pika.PlainCredentials("hit", "hit")))
            self.channel = connection.channel()
        except Exception as err:
            print str(err)

    def callback(self, ch, method, properties, body):
        try:
            print '[*] Receive message. %s' % body
            self.db_execute(body)  # 将获得的数据放入数据库中
        except Exception as e:
            print e
            return e

    def rabbitmq_comsumer(self):
        self.channel.queue_declare(queue='detection_result')
        self.channel.basic_consume(on_message_callback=self.callback, queue='detection_result', auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def gevent_pool(self, detection_result):
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
        for message_blocks in range(0, len(detection_result), split_num):
            messages = detection_result[message_blocks:message_blocks + split_num]
            for message in messages:
                tasks.append(p.spawn(detection_result, message))
            gevent.joinall(tasks)

        # for task in tasks:
        #     print task.value  # 返回的数据结构为tuple类型 (ip, [domains])
        #     self.channel.queue_declare(queue='dns_verification')
        #     self.channel.basic_publish(exchange='',
        #                                routing_key='dns_verification',
        #                                body=task.value)
        #     print 'send success'
    def db_execute(self, detection_result):
        detection_result = eval(detection_result)
        print " [*] recv message. ", detection_result
        origin_ip = detection_result[0][0]
        domain = detection_result[0][1]
        domain_ip = detection_result[0][2][0]
        malicious_type = detection_result[-1]
        table = 'malicious_ip_analysis_demo'
        sql = """INSERT INTO {table} (origin_ip, domain, domain_ip, malicious_type)
                VALUES('{origin_ip}', '{domain}', '{domain_ip}', '{malicious_type}')
              """.format(table=table, origin_ip=origin_ip, domain=domain,
                         domain_ip=domain_ip, malicious_type=malicious_type)
        print sql
        try:
            self.db.insert(sql)
        except Exception as e:
            print e


if __name__ == '__main__':
    DNSVerification().rabbitmq_comsumer()