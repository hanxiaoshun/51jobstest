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
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
date_time_str = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))

# ---------------------
job_df = []
jobs_info = []
uniq_company_jobs_info = []
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
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11傲游(Maxthon)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)腾讯TT',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)世界之窗(The World) 2.x',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)世界之窗(The World) 3.x',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)搜狗浏览器 1.x',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)360浏览器',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)Avant',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)Green Browser',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50IE 9.0'
]

# 设置一些比较稳定的IP代理(样例)
main_proxies = ['https://106.56.102.22:8070',
                'https://211.159.171.58:80', ]


class SpiderDomainInfo(object):
    """
    域名将详细文件手动转化成excel
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

    def load_uniq_detail_history(self):
        """
        加载历史数据
        :return:
        """
        try:
            files = "files"
            dirs = os.listdir("files")
            if dirs.__len__() > 0:
                for file in dirs:
                    if "detail" in file:
                        sub_file = os.path.join(files, file)
                        with open(sub_file, 'r', encoding='utf-8') as f:
                            if f.__sizeof__() > 0:
                                for line in f.readlines():
                                    if line.__len__() > 0:
                                        if "--==--==--" in line:
                                            line = line[:line.index('--==--==--')]
                                        lines = line.split('\t')
                                        if len(lines) > 0:
                                            company = lines[0]
                                            if company not in self.uniq_company:
                                                self.uniq_company.append(company)
                                                job_df.append(lines)
                                            else:
                                                pass
                                        else:
                                            pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
            else:
                pass
        except Exception as load_uniq_detail_e:
            input("make_excel 发生异常：" + str(load_uniq_detail_e))
            with open("files/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":load_uniq_detail 发生异常：" + str(load_uniq_detail_e))
            input("发生异常请记录一下错误并按任意键退出！")
            raise load_uniq_detail_e

    def make_excel(self):
        # print(job_df)
        try:
            page_path = 'excel'
            if os.path.exists(page_path):
                if len(os.listdir(page_path)) > 0:
                    for file in os.listdir(page_path):
                        os.remove(os.path.join(page_path, file))
            else:
                os.makedirs(page_path)

            data = pd.DataFrame(job_df)
            # 保存数据
            with pd.ExcelWriter(page_path + '/51jobs_' + date_time_str + '.xlsx') as writer:  # doctest: +SKIP
                data.to_excel(writer, sheet_name='51job', index=True, header=0, na_rep='')
        except Exception as make_excel_e:
            input("make_excel 发生异常：" + str(make_excel_e))
            with open("files/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":make_excel 发生异常：" + str(make_excel_e))
            input("发生异常请记录一下错误并按任意键退出！")
            raise make_excel_e

    def entrance(self):
        try:
            self.load_uniq_detail_history()
            self.make_excel()
        except Exception as entrance_e:
            print("entrance 发生异常：" + str(entrance_e))
            with open("files/51job_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":entrance 发生异常：" + str(entrance_e))
            input("发生异常请记录一下错误并按任意键退出！")
            raise entrance_e


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
    try:
        spider.entrance()
        end = time.time()
        print('Used time-->', end - start, 's')
    except Exception as main_e:
        print(str(main_e))
        with open("files/51job_error.txt", 'a', encoding='utf-8') as f_err:
            f_err.write(date_time_str + ":main 发生异常：" + str(main_e))
        input("发生异常请记录一下错误并按任意键退出！")
        raise main_e
    input('excel 文件已生成,请按任意键退出,或直接关闭窗口.')
