# encoding: utf-8

from DNS_Verification.resolving_ip_cname_by_dns import obtaining_domain_ip
from Third_party.ip_reverse import exper


def ip_check(ip):
    domains = exper(ip, spider_id=[1, 2, 3])
    ip_rst = []
    for domain in domains:
        ip_rst.append(obtaining_domain_ip(domain))
    print domains
    print ip_rst


if __name__ == '__main__':
    ip_check('61.135.169.121')