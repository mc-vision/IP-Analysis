# coding:utf-8
import schedule
import time
import threading
from malaedoaminlist import renzo
import MyDomains
from open_phish import renzo_op
from aa419 import renzo_aa
import vxvault_insert
import phishing_tank_download
import malicious_domain_summary
import anquanlianmeng


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

ma = renzo()
op = renzo_op()
aa = renzo_aa()

schedule.every().day.at("00:00").do(run_threaded,MyDomains.job1)
schedule.every().saturday.at("18:00").do(run_threaded,MyDomains.job2)
schedule.every().day.at("02:00").do(run_threaded,MyDomains.job3)
schedule.every().day.at("05:00").do(run_threaded,MyDomains.job4)
schedule.every().hour.do(run_threaded,phishing_tank_download.phishing_update)
schedule.every().day.at("08:00").do(run_threaded,vxvault_insert.mysql_handle)
schedule.every().day.at("10:00").do(run_threaded,op.Work)
schedule.every().day.at("11:00").do(run_threaded,anquanlianmeng.pattern)
schedule.every().day.at("23:00").do(run_threaded,anquanlianmeng.pattern)
schedule.every().day.at("12:00").do(run_threaded,ma.Work)
schedule.every().day.at("14:00").do(run_threaded,aa.Work)
schedule.every().monday.at("18:30").do(run_threaded,malicious_domain_summary.domain_summary)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
