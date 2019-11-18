# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from settings import phantomjs_path, chrome_path, USE_CHROME, Virtual_Display
from settings import Dailis_pool, USER_AGENTS
import random

# if USE_CHROME:
#     from pyvirtualdisplay import Display  # 环境搭建
#     enable_virtual_display = Virtual_Display
#     if enable_virtual_display:
#         display = Display(visible=0, size=(1920, 1080))
#         display.start()

dcap = dict(DesiredCapabilities.PHANTOMJS)  # 从库中随机选择浏览器头伪装浏览器


class BaseDriver(object):

    @staticmethod
    def init_phantomjs(timeout):
        # 定义浏览器头
        dcap["phantomjs.page.settings.loadImages"] = False
        dcap["phantomjs.page.settings.userAgent"] = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
        dcap["phantomjs.page.settings.resourceTimeout"] = timeout
        # 代理
        daili = Dailis_pool[random.randint(0,len(USER_AGENTS)-1)]
        daili = daili['ip']+':'+daili['port']
        if daili != '127.0.0.1:80':
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = daili
            proxy.add_to_capabilities(dcap)
            print "当前使用的代理是", daili
        dv = webdriver.PhantomJS(
            executable_path=phantomjs_path,
            desired_capabilities=dcap
        )
        dv.set_page_load_timeout(timeout)
        dv.set_script_timeout(timeout)

        return dv

    @staticmethod
    def init_chrome(timeout):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings": {
                'images': 2,
            }
        }
        chromeOptions.add_experimental_option("prefs", prefs)
        cur_daili = Dailis_pool[random.randint(0,len(Dailis_pool)-1)]
        user_agent = USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)]
        daili = cur_daili['type']+'://'+cur_daili['ip'] + ':' + cur_daili['port']
        chromeOptions.add_argument('--user-agent='+user_agent)
        if daili != "http://127.0.0.1:80":
            chromeOptions.add_argument('--proxy-server='+daili)
            print "当前使用的代理是", daili
        dv = webdriver.Chrome(executable_path=chrome_path,chrome_options=chromeOptions)
        dv.set_page_load_timeout(timeout)
        dv.set_script_timeout(timeout)

        return dv

    @staticmethod
    def init_driver(timeout):
        use_chrome = USE_CHROME
        return BaseDriver.init_chrome(timeout) if use_chrome else(BaseDriver.init_phantomjs(timeout))

    @staticmethod
    def quit_driver(dv):

        try:
            dv.quit()
        except Exception:
            return False
        else:
            return True

