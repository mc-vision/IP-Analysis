# -*- coding: utf-8 -*-
"""
功能：第三方工具检测恶意域名测试
作者：吴晓宝
日期:2018-1-26
"""

#from detect_tool import detect_tools
import detect_tools

def detect_malicious_exper():

    pro_tool_name = ''
    pro_result = ''
    pro_domain = ''
    count = 0
    dv = None
    print "+--------------开始测试-----------------+"
    while True:
        count += 1
        tool_name = raw_input("input tool_name/seq_num>> ").strip()
        if len(str(tool_name)) == 1:
            no = int(tool_name)
            if no == 1:
                tool_name = "sanliuling"#结果异常,异常
            elif no == 2:
                tool_name = "jinshan"#结果异常
            elif no == 3:
                tool_name = "tencent"#正常
            elif no == 4:
                tool_name = "baidu"#正常
            elif no == 5:
                tool_name = "macfree"#异常#完成_已正常
            elif no == 6:
                tool_name = "virustotal"#需要处理#已处理
            else:
                print "无此工具"
                print "+------------------------------------+"
                print "| detect tools selection:1/2/3/4/5/6 |"
                print "| tool-1 =>  sanliuling              |"
                print "| tool-2 =>  jinshan                 |"
                print "| tool-3 =>  tencent                 |"
                print "| tool-4 =>  baidu                   |"
                print "| tool-5 =>  macfree                 |"
                print "| tool-6 =>  virustotal              |"
                print "+------------------------------------+"
                continue
        if tool_name.strip().lower() == "sanliuling":
            source_class = detect_tools.Sanliuling
        elif tool_name == "jinshan":
            source_class = detect_tools.Jinshan
        elif tool_name == "tencent":
            source_class = detect_tools.TencentManager
        elif tool_name == "baidu":
            source_class = detect_tools.BaiduDefender
        elif tool_name == "macfree":
            source_class = detect_tools.Macfree
        elif tool_name == "virustotal":
            source_class = detect_tools.Virustotal
        else:
            if tool_name != "help":
                print "无此工具"
            print "+------------------------------------+"
            print "| detect tools selection:1/2/3/4/5/6 |"
            print "| tool-1 =>  sanliuling              |"
            print "| tool-2 =>  jinshan                 |"
            print "| tool-3 =>  tencent                 |"
            print "| tool-4 =>  baidu                   |"
            print "| tool-5 =>  macfree                 |"
            print "| tool-6 =>  virustotal              |"
            print "+------------------------------------+"
            if tool_name != "help":
                count = count - 1
            continue

        print "<=========%dth test start=======>" % (count)
        domain = raw_input("input domain>> ").strip()
        if pro_tool_name == tool_name and pro_domain == domain and pro_result != '检测失败#1'.decode('utf8'):
            print "%s detect domain %s result>>%s" % (tool_name, domain, pro_result)
        else:
            print "检测中..."
            print "wait %d seconds..." % (2 * source_class.wait_time)
            if tool_name in ['macfree', 'virustotal']:
                result = source_class.detect_malicious(domain)
                if result is None:
                    result = "检测失败#2"
                print "%s detect domain %s result>>%s" % (tool_name, domain, result)
                pro_result = result
                pro_tool_name = tool_name
            else:
                if dv is None or pro_result == '检测失败#3'.decode('utf8') or pro_tool_name != tool_name:
                    if tool_name=='baidu':
                        dv = source_class.driver_homeweb(dv=dv)
                    else:
                        dv = source_class.driver_homeweb(source_class.start_domain,dv=dv)
                dv,result = source_class.detect_malicious(domain,dv)
                if result is None:
                    result = "检测失败#4"
                print "%s detect domain %s result>>%s" % (tool_name, domain, result)
                pro_result = result
                pro_tool_name = tool_name
        print "<=========%dth test end========>" % count
        pro_domain = domain
        while True:
            flag = raw_input("quit yes or no?>> ").strip()
            if flag == 'yes':
                break
            elif flag == 'no':
                break
            else:
                print "please reinput yes or no!"
        if flag == 'yes':
            break
    if dv is not None:
        try:
            dv.quit()
        except Exception:
            pass
    print "+--------------测试结束-----------------+"

if __name__ == "__main__":
    detect_malicious_exper()
