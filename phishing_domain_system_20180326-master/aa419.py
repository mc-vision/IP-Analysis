#! usr/bin/python2.7
#coding=utf-8
import time
import re
import datetime
import MySQLdb
import requests
import schedule
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class renzo_aa:
    t = ""
    title = ""
    number = 0
    def GetTime(self):
         renzo_aa.t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         title = datetime.datetime.now().strftime("%Y-%m-%d")


    def GetNumber(self):
         url = "https://db.aa419.org/fakebankslist.php?start=1"
         reponse = requests.get(url)
         content = reponse.text
         getmaxinum = re.compile('<td><a href="fakebanksview.php\?key=(.*?)"><span class="phpmaker">')
         #<td><a href="fakebanksview.php?key=129233"><span class="phpmaker">
         maxinum = re.findall(getmaxinum, content)
         return int(maxinum[0])


    def GetPreId(self,filename):
         try:
              n=0        
              f = open(filename, "r")

              for line in f:
                   n = n + 1
                   if n == 1:
                        pre_id = line
              f.close()
              return int(pre_id)
         except:
              return 0

    
    def JudgeDiff(self,pre_id,new_id):
         if pre_id==new_id:
              return 0
         else:
              return 1


    def WriteNewId(self,filename, new_id):
         f = open(filename, "w")
         f.write(str(new_id))
         f.close()


    def SaveError(self, num):
        fe = open("error.txt", "a+")
        fe.write(str(num) + "\n")
        fe.close()


    def GetInfo(self,id):
         try:
              url = "https://db.aa419.org/fakebanksview.php?key=" + str(id)
              reponse = requests.get(url,timeout=60)
              content = reponse.text
              #print content
              getinfo = re.compile('''<th class="ewTableHeader">Url&nbsp;</th>[\S\s]*target="_blank">(.*?)</a> &nbsp[\S\s]*<th class="ewTableHeader">Domain&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Site Name&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Scam Type&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">SiteIP&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Web Host&nbsp;</th>[\S\s]*colspan="2">[\S\s]*&nbsp;</td>[\S\s]*<th class="ewTableHeader">ASNumber&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Status&nbsp;</th>[\S\s]*colspan="2">.*?&nbsp;</td>[\S\s]*<th class="ewTableHeader">Email&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Registrar&nbsp;</th>''')
              #--     <th class="ewTableHeader">Url&nbsp;</th>[\S\s]*target="_blank">(.*?)</a> &nbsp[\S\s]*
              #--     <th class="ewTableHeader">Domain&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
              #--     <th class="ewTableHeader">Site Name&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
              #--     <th class="ewTableHeader">Scam Type&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
              #--     <th class="ewTableHeader">SiteIP&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
              #++     <th class="ewTableHeader">Web Host&nbsp;</th>[\S\s]*colspan="2">[\S\s]*&nbsp;</td>[\S\s]*
              #--     <th class="ewTableHeader">ASNumber&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
              #++     <th class="ewTableHeader">Status&nbsp;</th>[\S\s]*colspan="2">.*?&nbsp;</td>[\S\s]*
              #--     <th class="ewTableHeader">Email&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*     
              #++     <th class="ewTableHeader">Registrar&nbsp;</th>
              info = re.findall(getinfo,content)
              #print info
         except:
              try:
                   getinfo = re.compile('''<th class="ewTableHeader">Url&nbsp;</th>[\S\s]*colspan="2">\n(.*?) <i>\(expired\)</i> &nbsp;[\S\s]*<th class="ewTableHeader">Domain&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Site Name&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Scam Type&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">SiteIP&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Web Host&nbsp;</th>[\S\s]*colspan="2">[\S\s]*&nbsp;</td>[\S\s]*<th class="ewTableHeader">ASNumber&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Status&nbsp;</th>[\S\s]*colspan="2">.*?&nbsp;</td>[\S\s]*<th class="ewTableHeader">Email&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*<th class="ewTableHeader">Registrar&nbsp;</th>''')
                   #getinfo = re.compile('''<th class="ewTableHeader">Url&nbsp;</th>[\S\s]*colspan="2">\n(.*?) <i>\(expired\)''')
                   #--     <th class="ewTableHeader">Url&nbsp;</th>[\S\s]*colspan="2">\n(.*?) <i>(expired)</i> &nbsp;[\S\s]*
                   #--     <th class="ewTableHeader">Domain&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
                   #--     <th class="ewTableHeader">Site Name&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
                   #--     <th class="ewTableHeader">Scam Type&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
                   #--     <th class="ewTableHeader">SiteIP&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
                   #++     <th class="ewTableHeader">Web Host&nbsp;</th>[\S\s]*colspan="2">[\S\s]*&nbsp;</td>[\S\s]*
                   #--     <th class="ewTableHeader">ASNumber&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*
                   #++     <th class="ewTableHeader">Status&nbsp;</th>[\S\s]*colspan="2">.*?&nbsp;</td>[\S\s]*
                   #--     <th class="ewTableHeader">Email&nbsp;</th>[\S\s]*colspan="2">(.*?)&nbsp;</td>[\S\s]*     
                   #++     <th class="ewTableHeader">Registrar&nbsp;</th>
                   info = re.findall(getinfo,content)
                   #print info
              except:
                   renzo_aa.SaveError(self,id)
                   return False

         return info[0]


    def Insert(self,infomation):
         #ip, user, password, dbname, charset = 'localhost', 'root', 'Shareck', 'renzotest', 'utf8'
         ip, user, password, dbname, charset = '10.245.146.39', 'root', 'platform', 'malicious_domain_collection', 'utf8'
         conn = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, charset=charset)
         cur = conn.cursor()
         cur.execute("insert into aa419(url, domain, insert_time, site_name, scam_type, site_ip, as_number, email) values(%s, %s, %s, %s, %s, %s, %s, %s)", (infomation[0], infomation[1], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), infomation[2], infomation[3], infomation[4], infomation[5], infomation[6]))
         cur.close()
         conn.commit()
         conn.close()
         '''

<tr>
<th class="ewTableHeader">Url&nbsp;</th>
<td class="ewTableAltRow" colspan="2">
http://www.advance-c-suisse.com <i>(expired)</i> &nbsp;
</td>
</tr>



<tr>
<th class="ewTableHeader">Url&nbsp;</th>
<td class="ewTableAltRow" colspan="2">
<a href="http://www.eminoc.com" rel="nofollow" target="_blank">http://www.eminoc.com</a> &nbsp;
</td>
</tr>


<tr>
<th class="ewTableHeader">Domain&nbsp;</th>
<td class="ewTableAltRow" colspan="2">eminoc.com&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Site Name&nbsp;</th>
<td class="ewTableAltRow" colspan="2">Emirates National Oil Company&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Scam Type&nbsp;</th>
<td class="ewTableAltRow" colspan="2">job (incl. reshipping &amp; money mule)&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">SiteIP&nbsp;</th>
<td class="ewTableAltRow" colspan="2">63.143.33.122&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Web Host&nbsp;</th>
<td class="ewTableAltRow" colspan="2">Date: 2018/01/16<br />
================<br />
IP 63.143.33.122 = AS46475 = Limestone Networks, Inc.&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">ASNumber&nbsp;</th>
<td class="ewTableAltRow" colspan="2">46475&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Status&nbsp;</th>
<td class="ewTableAltRow" colspan="2">active&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Email&nbsp;</th>
<td class="ewTableAltRow" colspan="2">shabconsult01@gmail.com&nbsp;</td>
</tr>
<tr>
<th class="ewTableHeader">Registrar&nbsp;</th>
<td class="ewTableAltRow" colspan="2">Pdr Ltd. D/b/a Publicdomainregistry.com&nbsp;</td>
</tr>
         '''


    def SendEmail(self,pre_id,new_id):#发送邮件
         #《输入》原、获取、重复、新增数据数目-《输出》发送信息反馈邮件
         try:
              msg_from = 'renshareck@aliyun.com'
              passwd = 'cP1052066743'
              msg_to = '1052066743@qq.com'
              subject = "Aa419Task"
              content1 = "Pre_id:%s,New_id:%s"%(str(pre_id),str(new_id))
              content2 = "\nIt's Over!\nMyLord!\n"
              content3 = "For Your Heart! My Honor!\n"
              content =content1 + content2 + content3
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


    def Job(self):
         filename = "id.txt"
         renzo_aa.GetTime(self)
         #print renzo.GetInfo(self,1)
         pre_id=renzo_aa.GetPreId(self,filename)
         new_id=renzo_aa.GetNumber(self)
         flag_diff=renzo_aa.JudgeDiff(self,pre_id,new_id)
         renzo_aa.WriteNewId(self,filename,new_id)
         renzo_aa.SendEmail(self,pre_id,new_id)
         if(flag_diff==1 and new_id>pre_id ):
              for i in range(pre_id+1,new_id+1):
                   if(i>pre_id):
                        info = renzo_aa.GetInfo(self,i)
                        if info != False:
                             renzo_aa.Insert(self,info)


    def Work(self):#工作main函数
          try:
               renzo_aa.Job(self)
          except:
               renzo_aa.Work(self)


if __name__ == "__main__":
     test = renzo_aa()
     schedule.every().day.at("12:00").do(test.Work)
     #schedule.every(1).minutes.do(test.Work)
     while True:
          schedule.run_pending()
          time.sleep(1)
