#! usr/bin/python2.7
#coding=utf-8

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


class renzo:
     t = ""
     title = ""
     filelog = "log.txt"#网站上次更新时间
     filename0 = ""#从网站上获取的数据
     filename1 = ""
     filename2 = ""
     urls = []
     domains = []
     ini_num = 0
     get_num = 0
     rep_num = 0
     add_num = 0
     flag_dif = 0#flag，0：网站未更新，1：网站已更新


     def GetTime(self):#获取时间
          #《输入》无-《输出》时间 title,t
          renzo.t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          title = datetime.datetime.now().strftime("%Y-%m-%d")


     def DownloadFile(self):#从网站下载文件
          #《输入》爬取对象网站url-《输出》txt数据文件 filename0
          url = 'http://www.malwaredomainlist.com/hostslist/hosts.txt'
          r = requests.get(url)
          renzo.filename0 = "hosts.txt"
          f0 = open(renzo.filename0, "w")
          f0.write(r.content)
          f0.close()


     def GetDiffFlag(self):#判断是否更新
          #《输入》上次的log.txt，下载的文件filename0-《输出》更新log.txt，变化flag flag_dif
          fl = open(renzo.filelog, "a+")
          f0 = open(renzo.filename0, "r")
          prelog = ""
          newlog = ""
          nl = n1 = 0
          #找出此次更新时间
          for line in f0:
               n1 = n1 + 1
               if(n1 == 3):
                    newlog = line
                    #print "newlog:%s"%newlog
          #找出上次更新时间
          for line in fl:
               nl = nl + 1
               if nl == 1:
                    prelog = line
                    #print "prelog:%s" % prelog
          fl.close()
          #对比，赋值flag_dif
          if (prelog == newlog):
               renzo.flag_dif = 0
          else:
               renzo.flag_dif = 1
          fl0 = open(renzo.filelog, "w")
          fl0.write(newlog)
          fl0.close()
          f0.close()


     def CutFile(self):#从下载文件中筛选出url信息
          #《输入》下载文件filename0-《输出》url存储文件filename1
          renzo.filename1 = renzo.t + "-hosts.txt"
          f0 = open(renzo.filename0, "r")
          f1 = open(renzo.filename1, "w")
          n0 = 0
          for line in f0:
               n0 = n0 + 1
               if(n0 > 6):
                    f1.write(line[11:])
          f0.close()
          f1.close()


     def DownloadDataBase(self):#从数据库下载数据
           #《输入》数据库信息-《输出》txt文件 filename2
          renzo.filename2 = renzo.t + "-data.txt"
          #ip, user, password, dbname, charset = 'localhost', 'root', 'Shareck', 'renzotest', 'utf8'
          ip, user, password, dbname, charset = '10.245.146.39', 'root', 'platform', 'malicious_domain_collection', 'utf8'
          conn = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, charset=charset)
          cur = conn.cursor()
          cur.execute("select url from malaedomainlist")
          m = cur.fetchall()
          f2 = open(renzo.filename2, "w")
          for n in m:
               #print str(n)[3:-3]
               f2.write(str(n)[3:-3]+"\n")
          f2.close()
          cur.close()
          conn.commit()
          conn.close()


     def GetDifferentUrls(self):#去重操作
           #《输入》两个txt文件-《输出》原数目、获取数、重复数、新增数、需插入的url init_num,get_num,rep_num,add_num, urls[]
          f1 = open(renzo.filename1, 'r')
          f2 = open(renzo.filename2, 'r')
          #set集合去重、计算数目
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
          renzo.ini_num = len(url2)
          renzo.get_num = len(url1)
          renzo.rep_num = len(repurl)
          renzo.add_num = len(addurl)
          for s in addurl:
               renzo.urls.append(s)


     def TurnDomain(self):#url转domain
          #《输入》待插入的url-#《输出》转换出的domain domains[]
          for url in renzo.urls:
               try:
                    domain = tld.get_tld(url)
               except:
                    urlcut = urlparse.urlparse(url)
                    temp = urlcut.netloc
                    domain = temp


     def Insert(self):#插入数据
          #《输入》数据库信息-《输出》数据库插入数据
          #ip, user, password, dbname, charset = 'localhost', 'root', 'Shareck', 'renzotest', 'utf8'
          ip, user, password, dbname, charset = '10.245.146.39', 'root', 'platform', 'malicious_domain_collection', 'utf8'
          conn = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, charset=charset)
          cur = conn.cursor()
          for i in range(0, len(renzo.urls)):
               cur.execute("insert into malaedomainlist(url, domain, insert_time ) values(%s, %s, %s)", (
                    renzo.urls[i].strip(), renzo.domains[i].strip(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
          try:
               cur.execute("alter table malaedomainlist drop column id")
               cur.execute("alter table malaedomainlist add id int")
               cur.execute("alter table malaedomainlist change id id int not null auto_increment primary key")
          except:
               cur.execute("alter table malaedomainlist add id int")
               cur.execute("alter table malaedomainlist change id id int not null auto_increment primary key")
          cur.close()
          conn.commit()
          conn.close()


     def SendEmail(self):#发送邮件
          #《输入》原、获取、重复、新增数据数目-《输出》发送信息反馈邮件
          try:
               msg_from = 'renshareck@aliyun.com'
               passwd = 'cP1052066743'
               msg_to = '1052066743@qq.com'
               subject = "Malaedomainlist Task"
               content0 = "The flag is:" + str(renzo.flag_dif) +"\n"
               content1 = "Initial urls (database) num:%s \nGet urls num:%s -renzo \nRepetitive urls num:%s \nAdditoinal urls num:%s -renzo \n"%(renzo.ini_num, renzo.get_num, renzo.rep_num, renzo.add_num)
               content2 = "\nIt's Over!\nGood evening!\nMyLord!\n"
               content3 = "For Your Heart! My Honor!\n"
               content = content0 + content1 + content2 + content3
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


     def RemoveFile(self):#删除文件
          #《输入》两个文件名-《输出》两个文件被删除
          #如果存在则删除
          if os.path.exists(renzo.filename0):
               os.remove(renzo.filename0)
          if os.path.exists(renzo.filename1):
               os.remove(renzo.filename1)
          if os.path.exists(renzo.filename2):
               os.remove(renzo.filename2)


     def Job(self):#main函数
          renzo.ini_num = 0
          renzo.get_num = 0
          renzo.rep_num = 0
          renzo.add_num = 0
          renzo.flag_dif = 0
          renzo.GetTime(self)
          renzo.DownloadFile(self)
          renzo.GetDiffFlag(self)
          if(renzo.flag_dif == 1):
               renzo.CutFile(self)
               renzo.DownloadDataBase(self)
               renzo.GetDifferentUrls(self)
               renzo.TurnDomain(self)
               renzo.Insert(self)
          else:
               print "No difference -renzo"
          renzo.SendEmail(self)
          renzo.RemoveFile(self)


     def Work(self):#工作main函数
          try:
               renzo.Job(self)
          except:
               renzo.RemoveFile(self)
               renzo.Work(self)


if __name__ == "__main__":
     test = renzo()
     test.Work()


