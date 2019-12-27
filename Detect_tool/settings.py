# -*- coding: utf-8 -*-

#driver settings

USE_CHROME = True
Virtual_Display = True

Dailis_pool = [
    {'type':'http','ip':'127.0.0.1','port':'80'},
    # {'type':'http','ip':'112.229.235.214','port':'8088'},
    # {'type':'http','ip':'121.8.98.198','port':'80'},
]#daili

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
]#agent

#executable_path
# phantomjs_path = 'C:\Users\wxb\Anaconda2\Scripts\phantomjs.exe'
# chrome_path = 'C:\Users\wxb\chromedriver\chromedriver.exe'
phantomjs_path = '/usr/bin/phantomjs2.2.1/bin/phantomjs'
chrome_path = 'D:/chromedriver'
