# -*- coding: utf-8 -*-
"""
功能：百度卫士进行恶意域名检测
作者：吴晓宝
日期:2018-1-13
"""
import multiprocessing
import time
from Driver_Base import BaseDriver


class BaiduDefender(object):
    """
    百度卫士检测网站危险程度
    """
    homeweb = 'http://bsb.baidu.com/diagnosis'
    timeout = 20
    wait_time = 2

    @staticmethod
    def driver_homeweb(dv=None,i=0):

        url = BaiduDefender.homeweb
        timeout = BaiduDefender.timeout
        wait_time = BaiduDefender.wait_time
        if dv is not None:
            BaseDriver.quit_driver(dv)
        dv = BaseDriver.init_driver(timeout)#初始化无头浏览器driver
        try:
            dv.get(url)
            time.sleep(wait_time)
        except Exception:
            return BaiduDefender.driver_homeweb(dv=dv,i=i+1)
        else:
            return dv

    @staticmethod
    def send_domain(domain,dv):

        try:
            dv.find_element_by_id('url').clear()
            dv.find_element_by_id('url').send_keys(domain)
            xpath = '//*[@id="search"]/div/div[3]/form/button'
            dv.find_element_by_xpath(xpath).click()
            time.sleep(BaiduDefender.wait_time)
        except Exception:
            dv = BaiduDefender.driver_homeweb(dv=dv)
            time.sleep(1)

        return dv

    @staticmethod
    def detect_malicious(domain,dv):
        result = None
        count = 0
        while not result:
            dv = BaiduDefender.send_domain(domain,dv)
            xpath = '//*[@id="result-icon"]/div'#查找元素
            res = dv.find_elements_by_xpath(xpath)
            #print('ok1')#
            #print(res[0].get_attribute('class').strip())#
            if len(res)!=0:
                result = res[0].get_attribute('class').strip()
                if result == "result_unknown":
                    result = "未知"
                elif result == "result_safety":
                    result = "安全"
                elif result == "result_danger":
                    result = "危险"
            else:
                dv = BaiduDefender.driver_homeweb(dv=dv)
            count += 1
            if count > 2:
                break

        return dv,result

    @staticmethod
    def detect_domain(domain):

        dv = BaiduDefender.driver_homeweb()
        # print ("%s detecting..."%domain)
        print domain,
        dv, result = BaiduDefender.detect_malicious(domain, dv)
        #print('return ok')#
        BaseDriver.quit_driver(dv)
        #print('quit ok')#
        return result

    @staticmethod
    def detect_domains(q, domains):

        dv = BaiduDefender.driver_homeweb()
        for i, domain in enumerate(domains):
            dv, result = BaiduDefender.detect_malicious(domain, dv)
            q.put(
                {
                    'domain': domain,
                    BaiduDefender.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (BaiduDefender.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (BaiduDefender.__name__, i + 1)
        q.put('quit')
        BaseDriver.quit_driver(dv)


if __name__ == "__main__":
    #单点测试
    domain_list = "baidu.com"
    domain_list=domain_list.splitlines()
    for domain in domain_list:
        print BaiduDefender.detect_domain(domain)
    # new types
