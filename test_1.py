# encoding: utf-8

from DNS_Verification.resolving_ip_cname_by_dns import obtaining_domain_ip
from Third_party.ip_reverse import exper
from Database.database import DB

import gevent


IP_POOL = """119.97.142.
    61.136.204.
    219.139.130.
"""
IP_POOL_1 = """120.202.25.
    61.136.241.
    219.148.37.
"""
IP_POOL_2 = """219.148.38.
    222.222.12.
    111.11.27.
"""
IP_POOL_3 = """39.108.50.
    183.232.43.
    183.61.19.
"""
IP_POOL_4 = """113.106.14.
    218.17.233.
    59.37.161.
"""


def ip_check(ip):
    domains = exper(ip, spider_id=[1, 2, 3])
    ip_domain_relations = []
    for domain in domains:
        ip_temp = obtaining_domain_ip(domain)
        for ip in ip_temp:
            ip_domain_relations.append([domain, ip_temp])

    for info in ip_domain_relations:
        domain, ip_final = info[0], info[1]
        if ip in ip_final:
            sql = """INSERT INTO ip_domains (origin_ip, domain, dns_ip) VALUES ('{ip_origin}', '{domain}', '{ip}') """.format(
                ip_origin=ip, domain=domain, ip=';'.join(ip_final)
            )
            print sql
            DB().insert(sql)
        else:
            sql = """INSERT INTO ip_domain_history (origin_ip, domain, dns_ip) VALUES ('{ip_origin}', '{domain}', '{ip}') """.format(
                ip_origin=ip, domain=domain, ip=';'.join(ip_final)
            )
            print sql
            DB().insert(sql)
            pass


def fun():
    print "fun start"
    gevent.sleep(0)

    for ip in IP_POOL.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip + str(i)
            ip_check(single_ip)


def fun_1():
    print "fun 1 start"
    gevent.sleep(0)

    for ip in IP_POOL_1.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip + str(i)
            ip_check(single_ip)


def fun_2():
    print "fun 2 start"
    gevent.sleep(0)

    for ip in IP_POOL_2.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip + str(i)
            ip_check(single_ip)


def fun_3():
    print "fun 3 start"
    gevent.sleep(0)

    for ip in IP_POOL_3.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip + str(i)
            ip_check(single_ip)


def fun_4():
    print "fun 4 start"
    gevent.sleep(0)

    for ip in IP_POOL_4.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip + str(i)
            ip_check(single_ip)


if __name__ == '__main__':
    # ip_check('61.135.169.121')
    """
    for ip in IP_POOL.splitlines():
        ip = ip.strip()
        print ip
        for i in range(256):
            single_ip = ip+str(i)
            ip_check(single_ip)
    """
    gevent.joinall([
        gevent.spawn(fun_1),
    ])

