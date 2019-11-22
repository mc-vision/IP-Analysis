import time
import MySQLdb
from datetime import datetime
from datetime import timedelta


def mysql_handle(table,time_limit_left,time_limit_right):
    timeArray_limit_left = time.strptime(time_limit_left, "%Y-%m-%d %H:%M:%S")
    timeStamp_limit_left = int(time.mktime(timeArray_limit_left))
    timeArray_limit_right = time.strptime(time_limit_right, "%Y-%m-%d %H:%M:%S")
    timeStamp_limit_right = int(time.mktime(timeArray_limit_right))
    db = MySQLdb.connect(
        "10.245.146.39", "root", "platform", "malicious_domain_collection")
    cursor = db.cursor()
    sql = "select domain,insert_time from " + table
    cursor.execute(sql)
    results = cursor.fetchall()
    flag_commit = 0
    for row in results:
        insert_time = str(row[1])
        domain = row[0]
        timeArray = time.strptime(insert_time, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        if timeStamp < timeStamp_limit_right and timeStamp > timeStamp_limit_left:
                value = [domain,insert_time,table]
                sql = "insert ignore into malicious_domain_collection_complete (domain,insert_time,domain_from) values(%s,%s,%s)"
                cursor.execute(sql, value)
                flag_commit = flag_commit + 1
                if flag_commit == 1000:
                    db.commit()
                    flag_commit = 0
        else:
            continue
    db.commit()
    db.close()


def get_date(days):
    return datetime.now() - timedelta(days=days)


def now_date():
    return datetime.now()


def domain_summary():
    gettime = str(now_date())[0:19]
    nowtime = str(get_date(7))[0:19]
    mysql_handle("aa419",nowtime,gettime)
    mysql_handle("cybercrime_tracker", nowtime, gettime)
    mysql_handle("hosts_domains", nowtime, gettime)
    mysql_handle("illegal_domains", nowtime, gettime)
    mysql_handle("malaedomainlist", nowtime, gettime)
    mysql_handle("malware_domains", nowtime, gettime)
    mysql_handle("open_phish", nowtime, gettime)
    mysql_handle("phishing_tank", nowtime, gettime)
    mysql_handle("vvx", nowtime, gettime)
    mysql_handle("weekly_domains", nowtime, gettime)
    mysql_handle("anquanlianmeng",nowtime,gettime)
    mysql_handle("malwaredb_malekal_domains", nowtime, gettime)
