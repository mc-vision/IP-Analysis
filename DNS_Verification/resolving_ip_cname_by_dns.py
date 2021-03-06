# encoding:utf-8

"""
利用dns递归服务器，解析出域名的IP
"""
import dns
import dns.resolver
import random
from Rabbitmq_list.MQ import rabbitmq
from Rabbitmq_list.MQ import ORIGIN_IP, MALICIOUS_DETECTION
MQ = rabbitmq()


class DomainRecord(object):
    """获取域名的DNS记录，默认本地递归服务器为1.2.4.8，超时时间为3s，重试次数为3次"""
    def __init__(self, original_domain, local_dns=None, timeout=2):
        self.original_domain = original_domain   # 原始域名
        self.ipv4, self.cnames = [], []
        self.ip_cname_status = 'FALSE'
        self.resolver = dns.resolver.Resolver(configure=False)
        self.resolver.timeout = timeout  # 超时时间
        self.resolver.lifetime = timeout*3  # 生命周期时间，即最多使用3个dns获取记录
        # self.resolver = dns.resolver.Resolver()  # 系统默认的递归服务器
        if local_dns:
            self.nameservers = [local_dns, '114.114.114.114', '223.5.5.5', '119.29.29.29', '180.76.76.76']  # 自定义本地递归服务器
        else:
            self.nameservers = ['114.114.114.114', '223.5.5.5', '119.29.29.29', '180.76.76.76']  # 自定义
        random.shuffle(self.nameservers)  # 随机
        self.resolver.nameservers = self.nameservers

    def fetch_rc_ttl(self):
        """获取域名的dns记录"""
        self.obtaining_a_cname_rc()

    def return_domain_rc(self):
        """返回域名的DNS记录"""
        return self.ipv4, self.cnames, self.ip_cname_status

    def obtaining_a_cname_rc(self):
        """
        获取域名的A和CNAME记录
        """
        try:
            resp_a = self.resolver.query(self.original_domain, 'A')
            for r in resp_a.response.answer:
                r = str(r.to_text())
                for i in r.split('\n'):  # 注意
                    i = i.split(' ')
                    rc_type, rc_data, rc_ttl = i[3], i[4], i[1]
                    if rc_type == 'A':
                        self.ipv4.append(rc_data)
                    elif rc_type == 'CNAME':
                        self.cnames.append(rc_data[:-1])
            self.ipv4.sort()
            self.ip_cname_status = "TRUE"
        except dns.resolver.NoAnswer:
            self.ip_cname_status = 'NO ANSWERS'
        except dns.resolver.NXDOMAIN:
            self.ip_cname_status = "NXDOMAIN"  # 尝试一次
        except dns.resolver.NoNameservers:
            self.ip_cname_status = 'NO NAMESERVERS'  # 尝试一次
        except dns.resolver.Timeout:
            self.ip_cname_status = 'TIMEOUT'
        except:
            self.ip_cname_status = 'UNEXPECTED ERRORS'


def obtaining_domain_ip(original_message, local_dns=None):
    """
    获取域名dns记录，local_dns：必须为列表
    :param original_message data structure (string(ip), list[domains])
    :return None
    """
    # print "received messages: ", original_message
    original_message = eval(original_message)
    original_ip = original_message[0]
    domain_list = original_message[1]
    for domain in domain_list:
        if local_dns is None:
            local_dns = []
        domain_obj = DomainRecord(domain, local_dns)
        domain_obj.fetch_rc_ttl()
        resloved_ip = domain_obj.return_domain_rc()[0]
        send_message = (original_ip, domain, resloved_ip)

        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='10.245.146.146', port=5672,
        #                               credentials=pika.PlainCredentials("hit", "hit")))
        # channel = connection.channel()
        # channel.queue_declare(queue='malicious_detection')
        # channel.basic_publish(exchange='',
        #                       routing_key='malicious_detection',
        #                       body=str(send_message))

        MQ.publish(data=send_message, queue=MALICIOUS_DETECTION)
        print("[x] Sent Success!"), send_message

        if original_ip != resloved_ip and resloved_ip != '':
            # 如果该IP为新增IP，则对其重新再次解析
            # connection = pika.BlockingConnection(
            #     pika.ConnectionParameters(host='10.245.146.146', port=5672,
            #                               credentials=pika.PlainCredentials("hit", "hit")))
            # channel = connection.channel()
            # channel.queue_declare(queue='origin_ip')
            # channel.basic_publish(exchange='',
            #                       routing_key='origin_ip',
            #                       body=str(resloved_ip))
            MQ.publish(data=str(resloved_ip), queue=ORIGIN_IP)
            print "[x] New IP send success!", resloved_ip


if __name__ == '__main__':
    # print obtaining_domain_ip('www.zhihu.com')
    obtaining_domain_ip("('204.11.56.48', ['iposei.com'])")
