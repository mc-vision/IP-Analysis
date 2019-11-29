# -*- coding: utf-8 -*-
import MySQLdb
from datetime import datetime
import re
import urllib
import tldextract
#import time
#import threading


def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


def url_extract(url):
    domain_extract = tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    if not suffix:
        insert = domain_extract
        return insert
    else:
        insert = domain_extract + '.' + suffix
        return insert


def pattern():
    #second =sleeptime(0,2,0)
    # time.sleep(second)
    con = MySQLdb.connect(host='10.245.146.39',
                          port=3306,
                          user='root',
                          passwd='platform',
                          db='malicious_domain_collection',
                          charset="utf8"
                          )
    cur = con.cursor()
    url = "https://jubao.anquan.org/exposure"
    ss = urllib.urlopen(url).read()
    pa2 = re.findall(r'<label.*?class="acc-info-name">(.*?)</label>', ss, re.S)
    pa1 = re.findall(r'<a.*?href="//www.anquan.org/s/(.*?)"', ss, re.I)
    pa3 = re.findall(r'<span.*?class="acc-info-type">(.*?)</span>', ss, re.S)
    pa4 = re.findall(r'<span.*?class="acc-info-time">(.*?)</span>', ss, re.S)
    pa5 = re.findall(
        r'<span.*?part-remark=".*?" full-remark="(.*?)" cur-state="part">.*?</span>', ss, re.S)
    # connest()
    for s1 in range(len(pa1)):
        pas = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pa = url_extract(pa1[s1])
        for s2 in range(len(pa2)):
            for s3 in range(len(pa3)):
                for s4 in range(len(pa4)):
                    for s5 in range(len(pa5)):
                        if s1 == s2 == s3 == s4 == s5:
                            p1 = str(pa1[s1])
                            p2 = str(pa)
                            p3 = str(pas)
                            p4 = str(pa4[s4])
                            p5 = str(pa3[s3])
                            p6 = str(pa5[s5])
                            cur.execute("REPLACE INTO anquanlianmeng(url,domain,insert_time,record_time,type,information) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                                p1, p2, p3, p4, p5, p6))
    cur.close()
    con.commit()
    con.close()
    #print 'ok'


if __name__ == "__main__":
    pattern()
