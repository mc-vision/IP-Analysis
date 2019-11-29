# -*- coding: utf-8 -*-
import urllib
import tldextract
import datetime
import MySQLdb
import time
from bs4 import BeautifulSoup
global url,domain,ip,md5,record_time


def beautifulsoup_get(start):
    try:
        res = urllib.urlopen("http://vxvault.net/ViriList.php?s=" + str(start) + "&m=100")
        soup = BeautifulSoup(res, "html.parser")
        page_div = soup.find(attrs={"id": "page"})
        return page_div
    except Exception, e:
        time.sleep(1)
        beautifulsoup_get(start)


def page_fonce_get(page_div,start):
    try:
        page_fonce = page_div.findAll(attrs={"class": "fonce"})
        return page_fonce
    except Exception, e:
        page_fonce_get(beautifulsoup_get(start),start)


def page_clair_get(page_div,start):
    try:
        page_clair = page_div.findAll(attrs={"class": "clair"})
        return page_clair
    except Exception, e:
        page_clair_get(beautifulsoup_get(start),start)


def url_extract(url):
    domain_extract = tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    if not suffix:
        insert = domain_extract
        return insert
    else:
        insert = domain_extract + '.' + suffix
        return insert


def mysql_insert(page,cursor,db):
    count_flag = 0
    insert_not = 0
    for line in page:
        if count_flag == 0:
            record_time = line.text
            count_flag = count_flag + 1
            continue
        elif count_flag == 1:
            url = line.text[4:]
            domain = url_extract(url)
            if url.strip()=='':
                insert_not = 1
            count_flag = count_flag + 1
            continue
        elif count_flag == 2:
            md5 = line.text
            count_flag = count_flag + 1
            continue
        elif count_flag == 3:
            ip = line.text
            count_flag = count_flag + 1
            continue
        elif count_flag == 4:
            count_flag = count_flag + 1
            continue
        elif count_flag == 5 and insert_not == 0:
            count_flag = 1
            record_time = line.text
            insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            value = [url, domain, ip, md5,record_time,insert_time]
            sql = "insert into vvx values(%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql, value)
                db.commit()
                continue
            except:
                continue
        elif count_flag == 5 and insert_not == 1:
            count_flag = 1
            insert_not = 0
            record_time = line.text
            continue


def mysql_handle():
    db = MySQLdb.connect(
        "10.245.146.39", "root", "platform", "malicious_domain_collection")
    cursor = db.cursor()
    page_count = 0
    insert(page_count, cursor, db)
    db.close()


def insert(page_count,cursor,db):
    page = page_count
    while (1):
        page_div = beautifulsoup_get(page)
        page_fonce = page_fonce_get(page_div, page)
        page_clair = page_clair_get(page_div, page)
        if page_fonce == [] and page_clair == []:
            break
        else:
            try:
                mysql_insert(page_fonce, cursor, db)
                mysql_insert(page_clair, cursor, db)
            except Exception, e:
                insert(page, cursor, db)
            page = page + 100


if __name__ == "__main__":
    mysql_handle()
