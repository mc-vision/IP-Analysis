#! usr/bin/python2.7
# coding=utf-8
import time
import datetime
import MySQLdb
import requests
import schedule
import urlparse
import os
import tld

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class renzo_op:
    t = ""
    title = ""
    filename1 = ""  # 从网站获取的url存储文件
    filename2 = ""  # 数据库的数据存储文件
    urls = []
    domains = []
    ini_num = 0  # 数据库中数据数目
    get_num = 0  # 从网站获取的数据数目
    rep_num = 0  # 重复的数据数目
    add_num = 0  # 新增的数据数目


    def GetTime(self):  # 获取时间
        #《输入》无-《输出》时间 title,t

        renzo_op.t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = datetime.datetime.now().strftime("%Y-%m-%d")


    def DownloadFile(self):  # 从网站下载文件
        #《输入》爬取对象网站url-《输出》txt数据文件 filename1
        url = 'https://openphish.com/feed.txt'
        r = requests.get(url)
        renzo_op.filename1 = renzo_op.t+"-feed.txt"
        f1 = open(renzo_op.filename1, "w")
        f1.write(r.content)
        f1.close()


    def DownloadDataBase(self):  # 从数据库下载数据
        #《输入》数据库信息-《输出》txt文件 filename2
        renzo_op.filename2 = renzo_op.t + "-data.txt"
        #ip, user, password, dbname, charset = 'localhost', 'root', 'Shareck', 'renzotest', 'utf8'
        ip, user, password, dbname, charset = '10.245.146.39', 'root', 'platform', 'malicious_domain_collection', 'utf8'
        conn = MySQLdb.connect(
            host=ip, user=user, passwd=password, db=dbname, charset=charset)
        cur = conn.cursor()
        cur.execute("select url from open_phish")
        m = cur.fetchall()
        f2 = open(renzo_op.filename2, "w")
        for n in m:
            # print type(n)
            # print str(n)
            # print str(n)[3:-3]
            f2.write(str(n)[3:-3]+"\n")
        f2.close()
        cur.close()
        conn.commit()
        conn.close()


    def GetDifferentUrls(self):  # 去重操作
        #《输入》两个txt文件-《输出》原数目、获取数、重复数、新增数、需插入的url init_num,get_num,rep_num,add_num, urls[]
        urls = []
        f1 = open(renzo_op.filename1, 'r')
        f2 = open(renzo_op.filename2, 'r')
        # set集合去重、计算数目
        url1 = set("")
        url2 = set("")
        for line1 in f1:
            url1.add(line1.strip())
        for line2 in f2:
            url2.add(line2.strip())
        f1.close()
        f2.close()
        repurl = url1 & url2
        addurl = url1 - url2
        renzo_op.ini_num = len(url2)
        renzo_op.get_num = len(url1)
        renzo_op.rep_num = len(repurl)
        renzo_op.add_num = len(addurl)
        for s in addurl:
            renzo_op.urls.append(s)


    def Error_TurnDomain_Error(self):  # 错误代码
        for url in renzo_op.urls:
            urlcut = urlparse.urlparse(url)
            temp = urlcut.netloc
            if "www." in temp:
                domain = temp.lstrip("www.")
            else:
                domain = temp
            renzo_op.domains.append(domain)


    def TurnDomain(self):  # url转domain
        #《输入》待插入的url-#《输出》转换出的domain domains[]
        domains = []
        for url in renzo_op.urls:
            try:
                domain = tld.get_tld(url)
            except:
                urlcut = urlparse.urlparse(url)
                temp = urlcut.netloc
                domain = temp
            renzo_op.domains.append(domain)


    def Insert(self):  # 插入数据
        #《输入》数据库信息-《输出》数据库插入数据
        #ip, user, password, dbname, charset = 'localhost', 'root', 'Shareck', 'renzotest', 'utf8'
        ip, user, password, dbname, charset = '10.245.146.39', 'root', 'platform', 'malicious_domain_collection', 'utf8'
        #ip, user, password, dbname, charset = '47.100.47.14', 'root', 'Shareck', 'renzotest', 'utf8'
        conn = MySQLdb.connect(
            host=ip, user=user, passwd=password, db=dbname, charset=charset)
        cur = conn.cursor()
        for i in range(0, len(renzo_op.urls)):
            cur.execute("insert into open_phish(url, domain, record_time, insert_time ) values(%s, %s, %s, %s)", (
                renzo_op.urls[i].strip(), renzo_op.domains[i].strip(
                ), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        try:
            cur.execute("alter table open_phish drop column id")
            cur.execute("alter table open_phish add id int")
            cur.execute(
                "alter table open_phish change id id int not null auto_increment primary key")
        except:
            cur.execute("alter table open_phish add id int")
            cur.execute(
                "alter table open_phish change id id int not null auto_increment primary key")
        cur.close()
        conn.commit()
        conn.close()


    def SendEmail(self):  # 发送邮件
        #《输入》原、获取、重复、新增数据数目-《输出》发送信息反馈邮件
        try:
            msg_from = 'renshareck@aliyun.com'
            passwd = 'cP1052066743'
            msg_to = '1052066743@qq.com'
            subject = "Open_phish Task"
            content1 = "Initial urls (database) num:%s \nGet urls num:%s \nRepetitive urls num:%s \nAdditoinal urls num:%s \n" % (
                renzo_op.ini_num, renzo_op.get_num, renzo_op.rep_num, renzo_op.add_num)
            content2 = "\nThe Day in The River!\nMy Lord!\n"
            content3 = "Please Take Yourself! My Honor!\n"
            content = content1 + content2 + content3
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = msg_from
            msg['To'] = msg_to
            email = smtplib.SMTP_SSL("smtp.aliyun.com", 465)
            email.login(msg_from, passwd)
            email.sendmail(msg_from, msg_to, msg.as_string())
            email.quit()
        except:
            print "Send error! Where is my owner? -Ran"


    def RemoveFile(self):  # 删除文件
        #《输入》两个文件名-《输出》两个文件被删除
        # 如果存在则删除
        if os.path.exists(renzo_op.filename1):
            os.remove(renzo_op.filename1)
        if os.path.exists(renzo_op.filename2):
            os.remove(renzo_op.filename2)


    def Job(self):  # main函数
        renzo_op.GetTime(self)
        renzo_op.DownloadFile(self)
        renzo_op.DownloadDataBase(self)
        renzo_op.GetDifferentUrls(self)
        renzo_op.TurnDomain(self)
        renzo_op.Insert(self)
        renzo_op.SendEmail(self)
        renzo_op.RemoveFile(self)


    def Work(self):  # 工作main函数
        try:
            renzo_op.Job(self)
        except:
            renzo_op.RemoveFile(self)
            renzo_op.Work(self)


if __name__ == "__main__":
     test = renzo_op()
     # test.Work()
     # schedule.every(1).minutes.do(test.Work)
     test.Work()
     # while True:
     #     schedule.run_pending()
     #     time.sleep(1)
