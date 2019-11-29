# coding:utf-8
from logging.handlers import HTTPHandler
from telnetlib import DEBUGLEVEL
from _socket import socket
from apscheduler.schedulers.background import BackgroundScheduler
import urllib
import urllib2
import re
import MySQLdb
import os
import time
import datetime
from ssl import cert_time_to_seconds
from warnings import catch_warnings
from pytz import HOUR
import tldextract


def fresh1(line):
    number1 = int(line.find('www.'))
    number2 = int(line.find('/'))
    if (number2 == -1):
        number2 = len(line)
    if (number1 != -1):
        number1 = number1 + 3
    s = line[number1 + 1:number2]
    return s


def fresh2(line):
    number1 = int(line.find('www.'))
    number2 = int(line.find(';'))
    if (number2 == -1):
        number2 = len(line)
    if (number1 != -1):
        number1 = number1 + 3
    s = line[number1 + 1:number2]
    return s


def url_extract(url):
    domain_extract = tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    if not suffix:
        insert = domain_extract
        return insert
    else:
        insert = domain_extract + '.' + suffix
        return insert
def fresh3(line):
    number1 = int(line.find(' '))
    s = line[number1 + 1:len(line)]
    return s


def urlfind(cur, table, url1):
    cur.execute("select url from " + str(table) + " where url = " + "'" + str(url1) + "'")
    rows = cur.fetchall()
    length = len(rows)
    return length

def urlinsert(cur, table, url1, domains, mal_type):
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "insert ignore into " + table + " values(" + "NULL" + "," + "'" + url1 + "'" + ',' + "'" + domains + "'" + "," + "'" + mal_type + "'" + "," + "'" + nowtime + "'" + ")" + ";")


def urlsfind(cur, table, urls1):
    cur.execute("SELECT urls FROM " + str(table) + " WHERE urls=" + "'" + str(urls1) + "'")
    rows = cur.fetchall()
    length = len(rows)
    return length


def urlread(cur,table):
    cur.execute("select url from " + str(table))
    OldUrls=set()
    rows=cur.fetchall()
    for line in rows:
        for line1 in line:
            OldUrls.add(line1)
    return  OldUrls


def urlsread(cur,table):
    cur.execute("select urls from " + str(table))
    rows=cur.fetchall()
    Oldurls=set()
    for line in rows:
        for line1 in line:
            Oldurls.add(line1)
    return  Oldurls


def urlsinsert(cur, table, urls, domains, mal_type):
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "insert ignore into " + table + " values(" + "NULL" + "," + "'" + urls + "'" + "," + "'" + domains + "'" + "," + "'" + mal_type + "'" + "," + "'" + nowtime + "'" + ")" + ";")


def joewein(cur,conn):  #
    urlList = []
    urlList.append('http://www.joewein.net/dl/dl/dom-bl-base.txt')
    urlList.append('http://www.joewein.net/dl/bl/dom-bl.txt')
    req = urllib2.Request(urlList[1])
    global JoeResponse
    try:
        JoeResponse = urllib2.urlopen(req, timeout=1000)
    except Exception as e:
      return 
    f = JoeResponse.readlines()
    JoeResponse.close()
    count=0
    NewUrls = set()
    for line in f:
        line = line.strip("\n")
        NewUrls.add(line)
    OldUrls=urlsread(cur,"weekly_domains")
    AllUrls = NewUrls | OldUrls
    UpdateUrls = AllUrls - OldUrls
    for line in UpdateUrls:
        if count<1000:
            domains = url_extract(line)
            urlsinsert(cur, 'weekly_domains', line, domains, 'spam domains')
            count=count+1
        else:
            conn.commit()
            count=0


def cybercrime(cur,conn):  # cybercrime
    req = urllib2.Request('http://cybercrime-tracker.net/all.php')
    global CybResponse
    try:
        CybResponse = urllib2.urlopen(req, timeout=1000)
    except Exception as e:
        return
    f = CybResponse.readlines()
    CybResponse.close()
    count=0
    NewUrls=set()
    for line in f:
        line = line.strip("\n")
        NewUrls.add(line)
    OldUrls = urlsread(cur, "cybercrime_tracker")
    AllUrls=NewUrls|OldUrls
    UpdateUrls = AllUrls - OldUrls
    for line in UpdateUrls:
        if count<1000:
            domains = url_extract(line)
            urlsinsert(cur, 'cybercrime_tracker', line, domains,"cibercrime")
            count=count+1
        else:
            conn.commit()
            count=0


def hosts(cur, conn):
    req = urllib2.Request('https://hosts.ubuntu101.co.za/hosts')
    global HostsResponse
    try:
        HostsResponse = urllib2.urlopen(req, timeout=10000)
    except Exception as e:
        return
    f = HostsResponse.readlines()
    HostsResponse.close()
    NewUrls=set()
    count = 0
    for line in f:
        if line[0] == '0':
            line = line.strip("\n")
            NewUrls.add(line)
    OldUrls=urlread(cur,"hosts_domains")
    AllUrls = NewUrls | OldUrls
    UpdateUrls = AllUrls - OldUrls
    for line in UpdateUrls:
        if count<1000:
           domains = url_extract(line)
           urlinsert(cur, 'hosts_domains', line, domains, 'malicious')
           count=count+1
        else:
            conn.commit()
            count=0


def malware(cur,conn):
    req = urllib2.Request('http://malwaredomains.lehigh.edu/files/justdomains')
    global MalResponse
    try:
        print
        "Request打开"
        MalResponse = urllib2.urlopen(req, timeout=100)
    except Exception as e:
        return
    f = MalResponse.readlines()
    MalResponse.close()
    count=0
    NewUrls=set()
    for line in f:
        line = line.strip("\n")
        NewUrls.add(line)
    OldUrls = urlsread(cur, "malware_domains")
    AllUrls = NewUrls|OldUrls
    UpdateUrls=AllUrls-OldUrls
    for line in UpdateUrls:
        if count<1000:
            domains = url_extract(line)
            urlsinsert(cur, 'malware_domains', line, domains, "malware")
            count=count+1
        else:
            conn.commit()
            count=0


def job1():
    conn = MySQLdb.connect(host='10.245.146.39', port=3306, user='root', passwd='platform',
                           db='malicious_domain_collection', charset='utf8')
    cur = conn.cursor()
    malware(cur,conn)
    cur.close()
    conn.commit()
    conn.close()


def job2():
    conn = MySQLdb.connect(host='10.245.146.39', port=3306, user='root', passwd='platform',
                           db='malicious_domain_collection', charset='utf8')
    cur = conn.cursor()
    joewein(cur,conn)
    cur.close()
    conn.commit()
    conn.close()


def job3():#Ϊhosts_domains
    conn = MySQLdb.connect(host='10.245.146.39', port=3306, user='root', passwd='platform',
                           db='malicious_domain_collection', charset='utf8')
    cur = conn.cursor()
    hosts(cur, conn)
    cur.close()
    conn.commit()
    conn.close()


def job4():#Ϊnew_cybercrime_tracker
    conn = MySQLdb.connect(host='10.245.146.39', port=3306, user='root', passwd='platform',
                           db='malicious_domain_collection', charset='utf8')
    cur = conn.cursor()
    cybercrime(cur,conn)
    cur.close()
    conn.commit()
    conn.close()


# schduler=BackgroundScheduler()
# schduler.add_job(job1,trigger='cron',hour='23',minute='00',second='00')
# schduler.add_job(job2,'cron',day_of_week='sat',hour=23,minute=00,second=00)
# schduler.add_job(job1,minute=1);
# schduler.add_job(job2,minute=2);
# schduler.start()
