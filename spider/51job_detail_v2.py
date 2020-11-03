#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 11:09
# @Author  : Hanxiaoshun@天谕传说
# @Site    : www.shunzi666.cn
# @File    :
# @Version    : 1.2
# @Mail    : 1425814646@qq.com
# @Software: PyCharm 2019.2
import json
import time
import requests
import re
import random
import os

from bs4 import BeautifulSoup
import math
import pandas as pd

date_time_str = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))

# ---------------------
job_df = []
jobs_info = []
# requests 的简单设置
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

requests.packages.urllib3.disable_warnings()
# 设置一些比较稳定的请求头信息，这个爬虫设置是非常重要的，
# 一些简单的反爬虫基本上会过滤请求头，如果是requests等爬虫工具的默认请求头，则很容易被禁
# 这样可以做到非常简单的伪装，以下是我简单搜集的请求头分享出来
main_user_agent = [
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50IE 9.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;IE 8.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)IE 7.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)IE 6.0',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)Firefox 4.0.1 – MAC',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1Firefox 4.0.1 – Windows',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1Opera 11.11 – MAC',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11Opera 11.11 – Windows',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11Chrome 17.0 – MAC',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11傲游(Maxthon)',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)腾讯TT',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)世界之窗(The World) 2.x',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)世界之窗(The World) 3.x',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)搜狗浏览器 1.x',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)360浏览器',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)Avant',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)Green Browser',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50IE 9.0',
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    # "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # "UCWEB7.0.2.37/28/999",
    # "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # "Openwave/ UCWEB7.0.2.37/28/999",
    # "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
]

# 设置一些比较稳定的IP代理(样例)
main_proxies = ['https://106.56.102.22:8070',
                'https://211.159.171.58:80', ]


class SpiderDomainInfo(object):
    """
    域名批量查询操作类
    """

    def __init__(self):
        """
        初始化参数信息
        """
        self.session = requests.session()
        self.cookies = requests.cookies.RequestsCookieJar()
        self.verify_URL = ""
        self.img_path = ""
        self.origin = ""
        self.host = ""
        self.accept = ""
        self.referer = ""
        self.getUrl = ""
        self.portUrl = ""
        self.verifyCode = 0
        self.payloadData = {}
        self.user_money = 0.0  # 用户的余额
        self.total_money = 0.0  # 本次批量订购的总价
        self.set_domain = set()
        self.pages = 0
        self.uniq_company = []
        self.uniq_company_jobs_info = []

    def cookie_fetch(self):
        """
        保存cookie
        :return:
        """
        main_header = {
            'User-Agent': user_agent,
            'Origin': self.origin,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        response = self.session.request('GET', url=self.referer, headers=main_header, cookies=self.cookies)
        # self.cookies.set('cookie-name', 'cookie-value', path='/', domain='.abc.com')  # 保存更新cookie
        self.session.cookies.update(response.cookies)

    def cookie_fetch_get(self):
        """
        保存cookie
        :return:
        """
        main_header = {
            'User-Agent': user_agent,
        }
        # response = self.session.request('GET', url=self.referer, headers=main_header)
        # print(response.text)
        # print(str(self.session.cookies.get_dict()))
        # self.cookies.set('cookie-name', 'cookie-value', path='/', domain='.abc.com')  # 保存更新cookie
        # self.session.cookies.update()

    def get_addr_detail(self):
        for job_info in self.uniq_company_jobs_info:
            detail_link_base = job_info[0:job_info.index('http')]
            detail_link_origin = job_info[job_info.index('http'):len(job_info)]
            self.get_addr_detail_link(detail_link_base, detail_link_origin)

    def get_addr_detail_link(self, detail_link_base, detail_link_origin):
        _link_origin = detail_link_origin
        sleep_second = 1 + random.randint(1, 6)
        print(detail_link_origin + ",等待执行：" + str(sleep_second) + "秒")
        time.sleep(sleep_second)
        try:
            search_header = {
                'User-Agent': str(random.choice(main_user_agent)),
            }
            res = self.session.get(
                detail_link_origin,
                # data=boss_params_detail,
                headers=search_header,
                proxies=None,
                timeout=25,
                allow_redirects=True,
                verify=False
            )
            res.encoding = res.apparent_encoding
            # print(str(res.text))
            job_detail_html = BeautifulSoup(res.text, features="html.parser")
            if job_detail_html.find("p", attrs={'class': 'fp'}):
                addr_detail = job_detail_html.find("p", attrs={'class': 'fp'}).text
                if addr_detail:
                    if "(邮编" in str(addr_detail).strip():
                        addr_detail_final = str(addr_detail).strip()
                        # print(addr_detail_final)
                        addr_detail_final = addr_detail_final[0:addr_detail_final.index('(邮编')]
                        detail_job_info = str(detail_link_base).strip() + "\t" + addr_detail_final.strip()
                    else:
                        detail_job_info = str(detail_link_base).strip() + "\t" + str(addr_detail).strip()
                else:
                    detail_job_info = str(detail_link_base).strip() + "\t" + "--==--==--"
                detail_job_str = str(detail_job_info).split("\t")
                # print(detail_job_str)
                job_df.append(detail_job_str)
                with open('files/51job_detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
            else:
                detail_job_info = str(detail_link_base).strip() + "\t" + "--==--==--"
                with open('files/51job_detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
        # print(detail_link_origin + ",完成")
        except Exception as get_addr_detail_e:
            print("get_addr_detail 发生异常：" + str(get_addr_detail_e))
            with open("log/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":get_addr_detail 发生异常：" + str(get_addr_detail_e) + '，异常链接：' +
                            str(detail_link_origin) + '\n')
            if 'latin-1' not in str(get_addr_detail_e):
                return self.get_addr_detail_link(detail_link_base, detail_link_origin)
            else:
                if 'gbk' not in str(get_addr_detail_e):
                    return self.get_addr_detail_link(detail_link_base, detail_link_origin)
                else:
                    pass

    def make_excel(self):
        # print(job_df)
        try:
            data = pd.DataFrame(job_df)
            # 保存数据
            with pd.ExcelWriter('files/51jobs_' + date_time_str + '.xlsx') as writer:  # doctest: +SKIP
                data.to_excel(writer, sheet_name='51job', index=True, header=0, na_rep='')
        except Exception as make_excel_e:
            input("make_excel 发生异常：" + str(make_excel_e))
            with open("log/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":make_excel 发生异常：" + str(make_excel_e) + '\n')
            if 'latin-1' not in str(make_excel_e):
                input("发生异常请记录一下错误并按任意键退出！")
                raise make_excel_e
            else:
                if 'gbk' not in str(make_excel_e):
                    input("发生异常请记录一下错误并按任意键退出！")
                    raise make_excel_e
                else:
                    pass

    def load_need_detail_data(self):
        """
        加载历史数据
        :return:
        """
        history_file = 'files/uniq_company.txt'
        num_1 = 0
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                if f.__sizeof__() > 0:
                    for line in f.readlines():
                        num_1 += 1
                        if num_1 < 3000:
                            line = line.replace('\n', '')
                            if line.__len__() > 0:
                                self.uniq_company_jobs_info.append(line)
                            # lines = line.split('\t')
                            # print(lines)
                            # if len(lines) > 0:
                            #     self.uniq_company_jobs_info.append(lines[0])
        else:
            with open(history_file, 'a', encoding='utf-8') as f:
                pass

    def load_history_data(self):
        """
        加载历史数据
        :return:
        """
        try:
            history_file = 'files/uniq_company.txt'
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    if f.__sizeof__() > 0:
                        for line in f.readlines():
                            line = line.replace('\n', '')
                            if line.__len__() > 0:
                                lines = line.split('\t')
                                # print(lines)
                                if len(lines) > 0:
                                    self.uniq_company.append(lines[0])
            else:
                with open(history_file, 'a', encoding='utf-8') as f:
                    pass
        except Exception as load_history_data_e:
            input("load_history_data 发生异常：" + str(load_history_data_e))
            with open("log/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":load_history_data 发生异常：" + str(load_history_data_e) + '\n')

            if 'latin-1' not in str(load_history_data_e):
                input("发生异常请记录一下错误并按任意键退出！")
                raise load_history_data_e
            else:
                if 'gbk' not in str(load_history_data_e):
                    input("发生异常请记录一下错误并按任意键退出！")
                    raise load_history_data_e
                else:
                    pass
        # print("ssss"+str(self.uniq_company))
        # input("继续.....")

    def entrance(self):
        try:
            # 与服务器通信握手
            # self.cookie_fetch()
            if not os.path.exists('log'):
                os.makedirs('log')
            else:
                pass

            # err_path = 'log/51job_error.txt".txt'
            # if os.path.exists(err_path):
            #     os.remove(err_path)
            # else:
            #     pass
            self.load_history_data()
            self.load_need_detail_data()
            self.get_addr_detail()
            self.make_excel()
        except Exception as entrance_e:
            print("entrance 发生异常：" + str(entrance_e))
            with open("log/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":entrance 发生异常：" + str(entrance_e) + "\n")
            if 'latin-1' not in str(entrance_e):
                input("发生异常请记录一下错误并按任意键退出！")
                raise entrance_e
            else:
                if 'gbk' not in str(entrance_e):
                    input("发生异常请记录一下错误并按任意键退出！")
                    raise entrance_e
                else:
                    pass


if __name__ == '__main__':
    """
    Boss直聘采集
    说明：
    1、处理待检测域名
    方法：
    """

    # 如果域名列表文件检查成功则继续，否则不继续...
    start = time.time()
    spider = SpiderDomainInfo()
    origin = 'https://www.51job.com/'
    referer = 'https://www.51job.com/'
    spider.origin = origin
    spider.referer = referer
    spider.getUrl = 'https://www.51job.com/'
    try:
        spider.entrance()
        end = time.time()
        print('Used time-->', end - start, 's')
    except Exception as main_e:
        print(str(main_e))
        with open("log/51job_error.txt", 'a', encoding='utf-8') as f_err:
            f_err.write(date_time_str + ":main 发生异常：" + str(main_e) + '\n')
        input("发生异常请记录一下错误并按任意键退出！")
        if 'latin-1' not in str(main_e):
            input("发生异常请记录一下错误并按任意键退出！")
            raise main_e
        else:
            if 'gbk' not in str(main_e):
                input("发生异常请记录一下错误并按任意键退出！")
                raise main_e
            else:
                pass
    input('按任意键退出,或关闭窗口.')
