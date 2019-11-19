# -*- coding: utf-8 -*-
"""
功能：360进行恶意域名检测
作者：吴晓宝
日期:2018-1-13
"""
import time
from Driver_Base import BaseDriver


class Sanliuling(object):
    """
    360检测网站是否具有木马病毒或诈骗
    """
    homeweb = 'https://webscan.qianxin.com/index/checkwebsite?url='
    start_domain = 'qq.com'
    timeout = 30  # 60
    wait_time = 15  # 15

    @staticmethod
    def driver_homeweb(domain,dv=None,i=0):

        url = Sanliuling.homeweb+domain
        timeout = Sanliuling.timeout
        wait_time = Sanliuling.wait_time
        if dv is not None:
            try:
                dv.delete_all_cookies()
            except Exception:
                pass
            BaseDriver.quit_driver(dv)
        dv = BaseDriver.init_driver(timeout)
        try:
            dv.get(url)
            time.sleep(wait_time)
        except Exception:
            return Sanliuling.driver_homeweb(domain,dv=dv,i=i+1)
        else:
            return dv

    @staticmethod
    def detect_domains(q, domains):

        dv = Sanliuling.driver_homeweb(Sanliuling.start_domain)
        for i, domain in enumerate(domains):
            dv, result = Sanliuling.detect_malicious(domain, dv)
            q.put(
                {
                    'domain': domain,
                    Sanliuling.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (Sanliuling.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (Sanliuling.__name__, i + 1)
        q.put('quit')
        BaseDriver.quit_driver(dv)

    @staticmethod
    def send_domain(domain,dv):

        try:
            dv.find_element_by_id('url').clear()
            dv.find_element_by_id('url').send_keys(domain)
            dv.find_element_by_xpath('//*[@id="checkwebsiteform"]/span').click()
            time.sleep(Sanliuling.wait_time)
        except Exception:
            dv = Sanliuling.driver_homeweb(domain, dv=dv)
            time.sleep(1)

        return dv

    @staticmethod
    def detect_malicious(domain,dv):

        result = None
        count = 0
        dv = Sanliuling.send_domain(domain,dv)
        while not result:
            limit_xpath = "/html/body/div[4]/div/p[1]"
            rs = dv.find_elements_by_xpath(limit_xpath)
            while len(rs) != 0 and rs[0].text.strip() == "大哥，你访问网站方式太像一个机器人了。你是怎么做到的！？".decode('utf8'):
                print "大哥，你访问网站方式太像一个机器人了。你是怎么做到的！？"
                dv = Sanliuling.driver_homeweb('qq.com', dv=dv)
                dv = Sanliuling.send_domain(domain,dv)
                count +=1
                print count
                if count > 2:
                    result = '检测失败'
                    break
                time.sleep(30)
                rs = dv.find_elements_by_xpath(limit_xpath)
            if count > 2:
                result = '检测失败'
                break
            weizhi_xpath = '//*[@id="webscan6"]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/dl[2]/dt'
            rs = dv.find_elements_by_xpath(weizhi_xpath)
            if len(rs) != 0 and rs[0].text.strip() == "网站还未认领，无法进行漏洞检测，安全得分未知".decode('utf8'):
                result = "网站还未认领，无法进行漏洞检测，安全得分未知"
            else:
                weijiance_xpath = '//*[@id="webscan6"]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/dl/dd'
                weizhijiance_xpath = '//*[@id="webscan6"]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/dl[2]/dd'
                rs1 = dv.find_elements_by_xpath(weijiance_xpath)
                rs2 = dv.find_elements_by_xpath(weizhijiance_xpath)
                if len(rs1) != 0 and rs1[0].text.strip() == "暂时没有发现被黑客入侵的痕迹，建议立即进行安全评估，领先黑客一步".decode('utf8'):
                    result = "你的网站已经几年未检测，建议立即检测".decode('utf8')
                elif len(rs2) != 0 and rs2[0].text.strip() == '检测后，可以发现潜在漏洞，并可一键进行修复，避免黑客入侵，保护网站安全'.decode('utf8'):
                    result = '没有进行过漏洞检测，安全得分未知'
                else:
                    xpath = '//*[@id="jg_tips"]'
                    res = dv.find_elements_by_xpath(xpath)
                    if len(res) != 0:
                        result = res[0].text.strip()
                    else:
                        dv = Sanliuling.driver_homeweb(domain, dv=dv)
                        time.sleep(Sanliuling.wait_time)
            try:
                dv.refresh()
            except Exception:
                pass

        return dv, result

    @staticmethod
    def detect_domain(domain):
        dv = Sanliuling.driver_homeweb(domain)
        print "检测中..."
        dv, result = Sanliuling.detect_malicious(domain, dv)
        BaseDriver.quit_driver(dv)

        return result


if __name__ == "__main__":
    domain = '0151b.com'  # '0411hy.com'
    print Sanliuling.detect_domain(domain)
