#-*- coding: UTF-8 -*-

"""
功能：virustotal进行域名的恶意性检测
作者：吴晓宝
日期:2018-1-13
"""
import requests
import time

class Virustotal():
    """
    使用virustotal检测网站是否有恶意木马程序
    """
    homeweb = 'https://www.virustotal.com/vtapi/v2/url/report'
    wait_time =  1
    list_api_key = [
        "713722fb9590cbeb51d82d1a9aa4d00063b002f38f42e2766364ddae21a4b65d",
        "f23e517d9ae196b8772dca29eb871790273ce99ad088fb88734791f05ce667f5",
        "f8a5d3f679b36a13fad4b43f9cb649c700f5943050816fb7818b9f067f108587",
        "49977ecd6f44702c6a7217c52ad77cc23fdb64a535721ae47f2d0a2c5aacd2c6",
        "d000b88b9b2825c946aebbce17f7dfe32fdee738ab5897c5fce8841f4cd16f67",
        "46d9901a482201dab2a288aeeca29af56c7d1818d9ee4e41b53de3545755b4d4",
        "b8507e4b55bd974a05bb255e3c8abc7e36af6cb76475d28664c12b5fa7186460",
        "0b0b6d76bcc0b8f83cae57414d59337c856d71a9f52edd72e266b5de123c39bd",
        "795ed87ac0a058d87b64628eb3b5853e1a8b10cb313cbe11d5ace1646a54dd8c",
        "49e6eb45fb532167519d9f157b34e6f5290978632a9d3f8cff231602c9b44c33",
        "5957c1a1d9bfd8598658012a57b1436db75f0437083df13400d887d475bf0b1e",
        "8012a5d0b746522e7af4f51577b23ce457189e5bea13c6144e06cd473805130b",
        "db9ce269f3893252366a209db7518f99110d9b6495eeabb0bb110a20fe0ed338",
        "7a74469b8db72a694f8c112297693c0b897ad6c7b73b3a8c4a046bf4af2a3161",
        "df0a463af2108ff010fd52bf74d1e2e11e03e0f2216f7f58c757dff53fbf5a5c"
    ]

    @staticmethod
    def api_use(domain, apikey,homeweb):
        '''
        调用 virustotal提供的api，查询目标url，返回查询结果
        '''
        try:
            params = {'apikey': apikey, 'resource': domain, 'allinfo': 'true'}
            response = requests.get(homeweb, params=params)
            api_data = response.json()
            if not api_data["scans"]:
                return 0
            else:
                return api_data["scans"]
        except:
            return 0

    @staticmethod
    def rate_count(api_dict):
        '''
        统计查询结果中的安全、未知、可疑的占比情况
        '''
        count = 0  # 总计数
        clean_count = 0  # 安全计数
        unrated_count = 0  # 未确定计数
        malicious_count = 0  # 可疑计数
        for scan_resource in api_dict:
            count = count + 1
            if api_dict[scan_resource]["result"] == "clean site":
                clean_count = clean_count + 1
            elif api_dict[scan_resource]["result"] == "unrated site":
                unrated_count = unrated_count + 1
            elif api_dict[scan_resource]["result"] == "malicious site":
                malicious_count = malicious_count + 1
        rate_clean = str(clean_count) + "/" + str(count)
        rate_unrated = str(unrated_count) + "/" + str(count)
        rate_malicious = str(malicious_count) + "/" + str(count)
        dict_return = {"clean": rate_clean,
                       "unrated": rate_unrated, "malicious": rate_malicious}

        return dict_return

    @staticmethod
    def organization_statistics(api_dict):
        '''
        将每个组织的检测情况拼接成字典
        '''
        dic_organization = {}
        for key in api_dict:
            dic_organization[key.encode("utf-8")] = api_dict[key]['result'].encode("utf-8")
        return dic_organization

    @staticmethod
    def detect_malicious(domain,i=0):

        time.sleep(Virustotal.wait_time)
        if i >= len(Virustotal.list_api_key):
            time.sleep(15)
            return None
        else:
            home_url = Virustotal.homeweb
            try:
                api_dict = Virustotal.api_use(domain, Virustotal.list_api_key[i],home_url)
            except Exception:
                return Virustotal.detect_malicious(domain, i + 1)
            else:
                if api_dict==0:
                    return Virustotal.detect_malicious(domain, i + 1)
                else:
                    dict_rate = Virustotal.rate_count(api_dict)
                    if isinstance(dict_rate, dict) and (dict_rate.get('malicious') != '' or dict_rate.get('unrated') != ''):
                        clean_rate = dict_rate.get('clean')#
                        malicious_rate = dict_rate.get('malicious')
                        unrated_rate = dict_rate.get('unrated')
                        site_dict = {'clean':clean_rate,'malicious rate':malicious_rate,'unrated_rate':unrated_rate,'malicious site':[],'unrated site':[]}
                        count = 0
                        detect_dict = Virustotal.organization_statistics(api_dict)
                        malicious_total = int(malicious_rate.split('/')[1])
                        for key, value in detect_dict.iteritems():

                            if count >= malicious_total:
                                break
                            if value in['malicious site','unrated site'] :
                                site_dict[value].append(key)
                        result = str(site_dict)

                        return result
                    else:
                        return Virustotal.detect_malicious(domain, i=i + 1)
    @staticmethod
    def detect_domain(domain):
        print "检测中..."
        return Virustotal.detect_malicious(domain)

    @staticmethod
    def detect_domains(q, domains):

        for i, domain in enumerate(domains):
            dv, result = Virustotal.detect_malicious(domain,i=i%len(Virustotal.list_api_key))
            q.put(
                {
                    'domain': domain,
                    Virustotal.__name__ + "_result": result
                }
            )
            print "--------------%s=>%d:start---------------" % (Virustotal.__name__, i + 1)
            print '{0}:{1}'.format(i + 1, domain)
            print result
            print "--------------%s=>%d:end-----------------" % (Virustotal.__name__, i + 1)
        q.put('quit')

if __name__ == "__main__":
    # 单点测试
    domain = '0000349.com'
    print Virustotal.detect_domain(domain)
