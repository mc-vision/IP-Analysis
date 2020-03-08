# encoding:utf-8

"""
说明：这个程序用来获得一些ip所绑定的域名集合，主要思路是从一些第三方网站直接获取
原始数据，经过解析后拿到域名集合，然后放入消息队列
This program is for getting domains of some bind ip address from web

Author @ wangjunxiong

"""
from ip_reverse import exper
# from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool  # 协程池
import gevent
import pika
from multiprocessing import Process  # 多进程
from Rabbitmq_list.MQ import rabbitmq
from Rabbitmq_list.MQ import ORIGIN_IP
MQ = rabbitmq()


class OriginIpReverse:
    def __init__(self):
        try:
            # connection = pika.BlockingConnection(
            #     pika.ConnectionParameters(host='10.245.146.146', port=5672,
            #                               credentials=pika.PlainCredentials("hit", "hit")))
            self.channel = MQ.new_channel()
        except Exception as err:
            print str(err)

    def callback(self, ch, method, properties, body):
        try:
            print '[*] Receive original ip. %s' % body
            self.gevent_pool(body.split('\n'))  # 将获得的数据放入协程池中
        except Exception as e:
            return e

    def rabbitmq_comsumer(self):
        self.channel.queue_declare(queue=ORIGIN_IP)
        self.channel.basic_consume(on_message_callback=self.callback, queue=ORIGIN_IP, auto_ack=True)
        print(' [*] Waiting for origin ipv4 address from MQ. data structure is string(ip) ')
        self.channel.start_consuming()

    def gevent_pool(self, origin_ip_set):
        """
        :param origin_ip_set:
        :return: None
        将消息队列接收到的域名按照分块大小放入协程池中，下面是几个重要参数
        coroutine_num: 协程数
        split_num: 块儿大小，即每一组放入到协程池中的总ip数量
        """
        coroutine_num = 10
        p = Pool(coroutine_num)
        split_num = 4
        tasks = []
        for ip_block in range(0, len(origin_ip_set), split_num):
            ip_set = origin_ip_set[ip_block:ip_block+split_num]
            for ip in ip_set:
                tasks.append(p.spawn(exper, ip, [1, 2, 3]))
            gevent.joinall(tasks)

        # for task in tasks:
        #     print task.value  # 返回的数据结构为tuple类型 (ip, [domains])
        #     self.channel.queue_declare(queue='dns_verification')
        #     self.channel.basic_publish(exchange='',
        #                                routing_key='dns_verification',
        #                                body=task.value)
        #     print 'send success'

    def mult_processing_mode(self, processing_num):
        """
        :param procrss_num: 进程数量
        :return: None
        """
        process_list = []
        for i in range(processing_num+1):  # 开启processing_num个子进程执行fun1函数
            p = Process(target=self.rabbitmq_comsumer, args=())  # 实例化进程对象
            p.start()
            process_list.append(p)

        for i in process_list:
            p.join()
        pass


if __name__ == '__main__':
    Task = OriginIpReverse()
    # processing_num = 4
    # process_list = []
    # for i in range(processing_num):  # 开启processing_num个子进程执行fun1函数
    #     p = Process(target=Task.rabbitmq_comsumer, args=())  # 实例化进程对象
    #     p.start()
    Task.rabbitmq_comsumer()
