# encoding: utf-8

from DNS_Verification.resolving_ip_cname_by_dns import obtaining_domain_ip
from Third_party.ip_reverse import exper
from Database.database import DB

import gevent


IP_POOL = """119.97.142.
    61.136.204.
    219.139.130.
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


def func():
    print "func start"

    for ip in IP_POOL.splitlines():
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
        gevent.spawn(func)
    ])

