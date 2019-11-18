#-*- coding: UTF-8 -*-

"""
功能：macfree进行域名的恶意性检测
作者：吴晓宝
日期:2018-1-13
"""

import urllib2
import time
from bs4 import BeautifulSoup

class Macfree():
    """
    macfree检测网站危险程度
    'High Risk','Medium Risk','Unverified','Minimal Risk'
    """
    homeweb = "https://www.mcafee.com/enterprise/en-us/threat-intelligence.domaintc.html?vid="
    timeout = 30
    wait_time = 2

    @staticmethod
    def detect_domains(q, domains):

        for i, domain in enumerate(domains):
            dv, result = Macfree.detect_malicious(domain)
            q.put(
                {
                    'domain': domain,
                    Macfree.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (Macfree.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (Macfree.__name__, i + 1)
        q.put('quit')

    @staticmethod
    def detect_malicious(domain):
        symbols = ['High','Medium','Minimal']
        result = None
        count = 0
        url = Macfree.homeweb + domain
        while not result:
            try:
                response = urllib2.urlopen(url, timeout=Macfree.timeout)
                soup_sourse=response.read()
                soup = BeautifulSoup(soup_sourse, 'html.parser')
                time.sleep(Macfree.wait_time)
                if soup is not None:
                    res = soup.find(name='img', attrs={'id': 'ctl00_breadcrumbContent_imgRisk'})
                    if res is not None:
                        result = res.attrs['title'].strip()
                        for r in symbols:
                            if r == result:
                                result = result + ' Risk'
                    if soup.find(name='span',attrs={'id': 'errorText'}).get_text()=='No results found. Please try again.':
                        result = 'No results found.'
                        break
                        
            except Exception:
                pass
            count +=1
            if count>2:
                break

        return result

    @staticmethod
    def detect_domain(domain):
        print "检测中..."
        return Macfree.detect_malicious(domain)


if __name__ == "__main__":
    # 单点测试
    domain = 'baidu.com'
    print Macfree.detect_domain(domain)
