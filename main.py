# encoding: utf-8

from DNS_Verification.resolving_ip_cname_by_dns import obtaining_domain_ip
from Third_party.ip_reverse import exper


def ip_check(ip):
    domains = exper(ip, spider_id=[1, 2, 3])
    ip_same, ip_diff = [], []
    for domain in domains:
        ip_temp = obtaining_domain_ip(domain)
        if ip in ip_temp:
            ip_same.append([domain, ip_temp])
        else:
            ip_diff.append([domain, ip_temp])

    for i in ip_same:
        print i
    print '\n'
    for item in ip_diff:
        print item


if __name__ == '__main__':
    ip_check('61.135.169.121')
