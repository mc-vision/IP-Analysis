# encoding:utf-8

"""
说明：这个程序用来获得一些ip所绑定的域名集合，主要思路是从一些第三方网站直接获取
原始数据，经过解析后拿到域名集合，然后放入消息队列
This program is for getting domains of some bind ip address from web

Author @ wangjunxiong

"""
from ip_reverse import exper
from gevent import monkey;monkey.patch_all()
import gevent
import pika
import multiprocessing


class Origin_Ip_Reverse:
    def __init__(self):
        pass

    def t(self):
        pass


if __name__ == '__main__':
    pass