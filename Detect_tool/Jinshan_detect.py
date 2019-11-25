# -*- coding: utf-8 -*-
"""
功能：金山卫士进行恶意域名检测
作者：吴晓宝
日期:2018-1-13
"""
import time
from Driver_Base import BaseDriver


class Jinshan(object):
    """
    金山卫士检测网站是否具有木马病毒或诈骗
    """
    homeweb = 'http://tool.chinaz.com/webscan?host='
    start_domain = 'qq.com'
    timeout = 30
    wait_time = 15
    max_time = 30

    @staticmethod
    def driver_homeweb(domain,dv=None,i=0):

        url = Jinshan.homeweb+domain
        timeout = Jinshan.timeout
        if dv is not None:
            BaseDriver.quit_driver(dv)
        dv = BaseDriver.init_driver(timeout)
        try:
            dv.get(url)
            time.sleep(1)
        except Exception:
            return Jinshan.driver_homeweb(domain,dv=dv,i=i+1)
        else:
            wait_time = Jinshan.wait_time
            time.sleep(wait_time)
            return dv

    @staticmethod
    def detect_domain(domain):

        dv = Jinshan.driver_homeweb(domain)
        print "检测中..."
        dv, result = Jinshan.detect_malicious(domain, dv)
        BaseDriver.quit_driver(dv)

        return result

    @staticmethod
    def detect_domains(q, domains):

        dv = Jinshan.driver_homeweb(Jinshan.start_domain)
        for i, domain in enumerate(domains):
            dv, result = Jinshan.detect_malicious(domain, dv)
            q.put(
                {
                    'domain': domain,
                    Jinshan.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (Jinshan.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (Jinshan.__name__, i + 1)
        q.put('quit')
        BaseDriver.quit_driver(dv)

    @staticmethod
    def detect_malicious(domain,dv):

        result = None
        try:
            dv.find_element_by_id('host').clear()
            dv.find_element_by_id('host').send_keys(domain)
            dv.find_element_by_xpath('//*[@id="webscan"]/div/div[2]/input').click()
            time.sleep(Jinshan.wait_time)
        except Exception:
            dv = Jinshan.driver_homeweb(domain, dv=dv)
            time.sleep(1)

        count = 0
        while not result:
            count+=1
            rss = dv.find_elements_by_xpath('//*[@id="form1"]/div[2]')
            while len(rss) != 0:
                st = rss[0].text.strip()
                if st == "被屏蔽的域名。".decode('utf8'):
                    return dv,st
                print st
                print domain
                dv.delete_all_cookies()
                dv = Jinshan.driver_homeweb(domain, dv=dv)
                time.sleep(1)
                rss = dv.find_elements_by_xpath('//*[@id="form1"]/div[2]')
            res = dv.find_elements_by_xpath('//*[@id="jstest"]/div[1]/h4')
            wait_time = 0
            while wait_time < Jinshan.max_time and len(res) == 0:
                print "sleep %d seconds..." % Jinshan.wait_time
                time.sleep(Jinshan.wait_time)
                res = dv.find_elements_by_xpath('//*[@id="jstest"]/div[1]/h4')
                wait_time += Jinshan.wait_time
            if len(res) != 0:
                result = res[0].text.strip()
            if count>3:
                break
        return dv,result


if __name__ == "__main__":
    domain = 'weihaiexpo.cn'
    print Jinshan.detect_domain(domain)