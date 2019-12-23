# encoding: utf-8
"""
同a/ip记录反查域名，通过第三方网站进行ip的反查
"""
import sys
sys.setrecursionlimit(10000)
from datetime import datetime
from bs4 import BeautifulSoup
from driverhandler import DriverHandler
from tldextract import extract
from ip_set import ips
import urllib2
import time
import sys
from gevent.pool import Pool
from gevent import monkey
import gevent
monkey.patch_all()
success = 0
failed = 0


class BGPSpider(DriverHandler):
    """
    https://bgp.he.net/ip/43.229.6.43#_dns
    """

    def __init__(self, timeout=60):

        DriverHandler.__init__(self, 'chrome', max_time=timeout)
        self.result = {}
        self.counter=0
        self.base_url = 'https://bgp.he.net/ip/{ip}#_dns'

    def spider(self, ip):

        self.counter+=1
        if not self.result.get(ip):
            self.result[ip] = {}
            self.result[ip]['cur_time'] = datetime.now()
        url=self.base_url.format(ip=ip)
        domains=set()
        flag=self.open_web(url)
        if flag:
            try:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
            except Exception, e:
                print "parse error:",str(e)
            else:
                div_tip = soup.find(name='div', attrs={'id': 'dns'})
                if div_tip:
                    a_tips = div_tip.find_all(name='a', title=True)
                    for a_tip in a_tips:
                        domain = a_tip.attrs['title'].strip()
                        domains.add(domain)
        if not flag or self.counter%10==0:
            self.destory_driver()
            self.create_driver()
            self.counter=0
        self.result[ip]['domains']=domains
        result=dict(ip=ip,**self.result[ip])
        del self.result[ip]

        return result


class DomainBigDataSpider(object):
    """
    https://domainbigdata.com/
    """

    def __init__(self, timeout=10,wait_time=1):

        self.result = {}
        self.base_url = 'https://domainbigdata.com/{ip}'
        self.timeout = timeout
        self.wait_time=wait_time

    def spider(self, ip):
        """

        :param ip:
        :return:
        """
        domains=set()
        if not self.result.has_key(ip):
            self.result[ip] = {}
            self.result[ip]['cur_time']=datetime.now()
        try:
            response = urllib2.urlopen(self.base_url.format(ip=ip), timeout=self.timeout)
            time.sleep(self.wait_time)
        except Exception, e:
            print "get error:",str(e)
        else:
            try:
                soup = BeautifulSoup(response, 'lxml')
            except Exception,e:
                print "parse error:",str(e)
            else:
                lis = soup.find(name='div', attrs={'id': 'MainMaster_divRptDomainsOnSameIP'})
                if lis:
                    a_tips = lis.find_all(name='a', href=True)
                    domains = domains|set([a_tip.text.strip() for a_tip in a_tips])
        self.result[ip]['domains']=domains
        result = dict(ip=ip, **self.result[ip])
        del self.result[ip]

        return result


class AizhanSpider(object):
    """
    dns.aizhan.com　
    """

    def __init__(self, timeout=5, wait_time=2):

        self.base_url = "https://dns.aizhan.com/%s/%d/"  # 基址
        self.timeout = timeout
        self.wait_time = wait_time

    def spider(self, ip, page_index=0):
        """
        获取页面源
        :param ip:
        :param page_index:
        :return:
        """
        if page_index<0:
            print "page index is error!"
            sys.exit(-1)
        # print "spider the %dth page"%(page_index+1)
        if page_index == 0:
            self.page_num = -1
            self.result = {}
        if not self.result.has_key(ip):
            self.result[ip] = {}
            self.result[ip]['cur_time']=datetime.now()
            self.result[ip]['domains']=set()
        if page_index==0 or page_index < self.page_num:
            url = self.base_url % (ip, page_index)
            try:
                response = urllib2.urlopen(url, timeout=self.timeout)
                time.sleep(self.wait_time)  # 等待数据加载
            except Exception, e:
                print "get error:",str(e)
            else:
                try:
                    soup = BeautifulSoup(response, 'lxml')
                except Exception, e:
                    print "parse error:", str(e)
                else:
                    if page_index == 0:
                        ul_tip=soup.find(name='div',attrs={'class':'dns-infos'}).ul
                        if ul_tip:
                            lis=ul_tip.find_all(name='li')
                            if len(lis)==3:
                                domains_num=int(lis[2].span.text.strip())
                                self.page_num=domains_num//20
                                if domains_num%20!=0:self.page_num+=1
                                # print "has %d pages"%self.page_num
                    domains_tip=soup.find_all(name='td',attrs={'class':'domain'})[1:]
                    for domain_tip in domains_tip:
                        domain=domain_tip.a.text.strip()
                        domain=extract(domain).registered_domain
                        if domain:
                            self.result[ip]['domains'].add(domain)
            self.spider(ip,page_index=page_index+1)

        result = self.result[ip]

        return dict(ip=ip, **result)


def exper(ip, spider_id):
    global success, failed
    generator, rst = [], []
    ip = str(ip)
    print ip
    if 1 in spider_id:
        bgp=BGPSpider()
        # print bgp.spider(ip)
        generator.append(i for i in bgp.spider(ip)['domains'])
        bgp.destory_driver()
    if 2 in spider_id:
        dbd=DomainBigDataSpider()
        # print dbd.spider(ip)
        generator.append(i for i in dbd.spider(ip)['domains'])
    if 3 in spider_id:
        aizhan=AizhanSpider()
        # print aizhan.spider(ip)
        generator.append(i for i in aizhan.spider(ip)['domains'])
    for domains in generator:
        for domain in domains:
            rst.append(domain)
    if rst != []:
        success += 1
    else:
        failed += 1
    print ip, rst


def coroutine_exper(origin_ip):
    global success, failed
    f = open('chrome_speed.txt', 'a+')
    coroutine_num = 5
    for coroutine_now in range(coroutine_num, 41, 3):
        p = Pool(coroutine_now)
        split_num = 5
        jobs = []
        start = time.time()
        # print origin_ip
        for num in range(0, len(origin_ip), split_num):
            origin_ip_set = origin_ip[num:num + split_num]
            for ip in origin_ip_set:
                jobs.append(p.spawn(exper, ip, [1, 2, 3]))
            print "coroutine start!"
            gevent.joinall(jobs)
            print success, " ", failed
        print >>f, str(coroutine_now) + ' ' + str(success) + ' ' + str(failed) + ' ' + str(time.time() - start) + ' ' +\
            str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print str(coroutine_now) + ' ' + str(success) + ' ' + str(failed) + ' ' + str(time.time() - start) + ' ' + str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        success, failed = 0, 0
    f.close()


if __name__ == "__main__":
    # print exper('119.97.142.82', spider_id=[1, 2, 3])
    ips = ips.split('\n')
    while True:
        coroutine_exper(ips)
