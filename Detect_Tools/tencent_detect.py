# -*- coding: utf-8 -*-
"""
功能：腾讯管家进行恶意域名检测
作者：吴晓宝
日期:2018-1-13
"""
import time
from Driver_Base import BaseDriver


class TencentManager(object):
    """
    腾讯管家检测网站恶意类型
    """
    homeweb = 'https://guanjia.qq.com/online_server/result.html?url='
    start_domain = 'qq.com'
    timeout = 30
    wait_time = 2

    @staticmethod
    def driver_homeweb(domain,dv=None,i=0):

        url = TencentManager.homeweb+domain
        timeout = TencentManager.timeout
        wait_time = TencentManager.wait_time
        if dv is not None:
            BaseDriver.quit_driver(dv)
        dv = BaseDriver.init_driver(timeout)
        try:
            dv.get(url)
            time.sleep(wait_time)
        except Exception:
            return TencentManager.driver_homeweb(domain,dv=dv,i=i+1)
        else:
            return dv

    @staticmethod
    def detect_domains(q, domains):

        dv = TencentManager.driver_homeweb(TencentManager.start_domain)
        for i, domain in enumerate(domains):
            dv, result = TencentManager.detect_malicious(domain, dv)
            q.put(
                {
                    'domain': domain,
                    TencentManager.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (TencentManager.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (TencentManager.__name__, i + 1)
        q.put('quit')
        BaseDriver.quit_driver(dv)

    @staticmethod
    def send_domain(domain,dv):

        try:
            dv.find_element_by_id('url').clear()
            dv.find_element_by_id('url').send_keys(domain)
            dv.find_element_by_xpath('//*[@id="checkwebsiteform"]/span').click()
            time.sleep(TencentManager.wait_time)
        except Exception:
            dv = TencentManager.driver_homeweb(domain, dv=dv)
            time.sleep(1)

        return dv

    @staticmethod
    def detect_malicious(domain,dv):

        result =  None
        count = 0
        while not result:
            dv = TencentManager.send_domain(domain,dv)
            res = dv.find_elements_by_xpath('//*[@id="score_img"]/span')
            if len(res)!=0:
                result = res[0].text.strip()
            else:
                dv = TencentManager.driver_homeweb(domain,dv=dv)
            count += 1
            if count > 2:
                break

        return dv, result

    @staticmethod
    def detect_domain(domain):

        dv = TencentManager.driver_homeweb(TencentManager.start_domain)
        print "检测中..."
        dv, result = TencentManager.detect_malicious(domain, dv)
        BaseDriver.quit_driver(dv)

        return result


if __name__ == "__main__":
    # 单点测试
    domain = 'weihaiexpo.cn'
    print TencentManager.detect_domain(domain)
