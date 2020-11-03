# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 11:09
# @Author  : Hanxiaoshun@天谕传说
# @Site    : www.shunzi666.cn
# @File    : batch_domain.py
# @Version    : 1.5 增加弹出框以及提交结算
# @Mail    : 1425814646@qq.com
# @Software: PyCharm 2019.2

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import uuid
import time
import json
import time
import requests
import re
import random
import os
import math
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import math
import pandas as pd

job_df = []
jobs_info = []

# 请求头和cookie设置
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

chrome_options = Options()
# 不弹出浏览器模式，不弹出浏览器模式默认网页size
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--user-agent=' + user_agent)
chrome_options.add_argument('--disable-infobars')

# chrome_options.add_argument('--proxy-server={}'.format(proxy))
# # 配置忽略ssl错误
# capabilities = DesiredCapabilities.CHROME.copy()
# capabilities['acceptSslCerts'] = True
# capabilities['acceptInsecureCerts'] = True
# browser = webdriver.Chrome(desired_capabilities=capabilities)
chrome_driver = 'Application/chromedriver.exe'  # 手动指定使用的浏览器位置

# chrome_driver = r"C:\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

# 不弹出浏览器模式，不弹出浏览器模式默认网页size
# driver = webdriver.Chrome(executable_path=chrome_driver)

date_time_str = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))

# requests 的简单设置
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
requests.packages.urllib3.disable_warnings()
# 设置一些比较稳定的请求头信息，这个爬虫设置是非常重要的，
# 一些简单的反爬虫基本上会过滤请求头，如果是requests等爬虫工具的默认请求头，则很容易被禁
# 这样可以做到非常简单的伪装，以下是我简单搜集的请求头分享出来(样例待用)
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

main_proxies_https = ['https://163.204.241.204:9999',
                      'https://163.204.244.81:9999',
                      'https://222.89.32.156:9999',
                      'https://123.163.96.103:9999',
                      'https://49.73.113.250:9999',
                      'https://120.83.105.189	:9999',
                      'https://182.34.33.111:9999',
                      'https://49.73.113.11:9999',
                      'https://113.195.225.13:9999',
                      'https://106.56.102.22:9999',
                      'https://112.85.166.64:9999',
                      'https://163.204.247.232:9999',
                      'https://182.35.86.95:9999']

main_proxies_http = ['http://110.86.136.102:9999',
                     'http://163.204.245.15:9999',
                     'http://163.204.245.185:9999',
                     'http://60.13.42.249:9999',
                     'http://163.204.241.135:9999',
                     'http://171.12.113.206:9999',
                     'http://58.253.155.214:9999']

# 设置一些比较稳定的IP代理(样例待用)
main_proxies = ['https://106.56.102.22:8070',
                'https://211.159.171.58:80', ]


class SelenuimTool(object):
    """
    Selenuim 工作区间
    """

    def __init__(self):
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

    def get_html_source(self, ready_url):
        driver.get(ready_url)
        time.sleep(1)
        print(driver.page_source)
        return driver.page_source

    def login_with_verify_picture(self, ready_url, width, height, delay, picture_code, refresh=False):
        try:
            ready_search = False
            # driver.set_window_size(width, height)
            driver.get(ready_url[0])
            all_w0 = driver.window_handles
            print('所有窗口0', all_w0)
            cookies = driver.get_cookies()
            print("登录之前的cookie：%s " % str(cookies))
            print("登录之前的url：%s " % driver.current_url)
            login_before_current_url = driver.current_url
            img = driver.find_element_by_id("imgid")
            all_w2 = None
            if img:
                # 存在则证明还尚未登录，尚未跳转，需重新登录，否则应表示为已通过，除非网页断网
                # img.click()
                if not os.path.exists("verify_img"):
                    os.makedirs("verify_img")
                else:
                    pass

                    print("verify_code: %s" % self.verify_code)
                    input_xpath_username = '//*[@id="input_register"]'
                    input_xpath_pwd = '//*[@id="input_registera"]'
                    input_xpath_code = '//*[@id="input_registerb"]'
                    enter_xpath = '//*[@id="denglu_button"]'

                    input_code = self.verify_code

                    # selenuimTool.selenium_event_input(seed_url, input_xpath, input_content, enter_xpath)
                    element_input = driver.find_element_by_xpath(input_xpath_username)
                    element_input.clear()
                    element_input.send_keys()
                    element_input = driver.find_element_by_xpath(input_xpath_pwd)
                    element_input.clear()
                    element_input.send_keys()
                    element_input = driver.find_element_by_xpath(input_xpath_code)
                    element_input.clear()
                    element_input.send_keys(input_code)
                    # element.send_keys(Keys.RETURN)
                    element_enter = driver.find_element_by_xpath(enter_xpath)

                    # 第一次获取所有窗口
                    all_w1 = driver.window_handles
                    print('所有窗口1', all_w1)
                    element_enter.click()
                    # 获取当前窗口
                    current_window1 = driver.current_window_handle
                    # 默认第一个窗口
                    print('第一个窗口', current_window1)
                    # 第二次获取所有窗口后发现 多了一个
                    all_w2 = driver.window_handles
                    cookies = driver.get_cookies()
                    print("登录之后的cookie：%s " % str(cookies))
                    login_after_current_url = driver.current_url
                    print("登录之后的url：%s " % login_after_current_url)

                    quit_button = EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div/div[1]/div[2]/div/ul[2]/li[8]/div/a/span"))
                    if quit_button:
                        ready_search = True
                    else:
                        pass
        except Exception as ee:
            raise ee

    def boss_zhipin(self, ready_url):
        print(ready_url)
        driver.get(ready_url)
        time.sleep(2)
        print(driver.current_url)
        print(driver.page_source)
        # 首页
        print('1、current window: %s ' % driver.current_window_handle)
        print('1、current window_handles: %s ' % driver.window_handles)
        print('1、current cookies %s' % driver.get_cookies())

        element_input = driver.find_element_by_xpath('//*[@id="wrap"]/div[4]/div/div/div[1]/form/div[2]/p/input')
        element_input.clear()
        element_input.send_keys('外贸')
        # 搜索外贸
        element_input = driver.find_element_by_xpath('//*[@id="wrap"]/div[4]/div/div/div[1]/form/button')
        time.sleep(1)
        element_input.click()
        time.sleep(3)
        print('2、current window: %s ' % driver.current_window_handle)
        print('2、current window_handles: %s ' % driver.window_handles)
        print('2、current cookies %s' % driver.get_cookies())

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        # 选择城市
        element_input = driver.find_element_by_xpath('//*[@id="filter-box"]/div/div[2]/dl[1]/dd/a[7]')
        time.sleep(1)
        element_input.click()

        print('3、current window: %s ' % driver.current_window_handle)
        print('3、current window_handles: %s ' % driver.window_handles)
        print('3、current cookies %s' % driver.get_cookies())

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # job_divs = driver.find_element_by_class_name('job-primary')
        #
        # for div in job_divs:

        html = BeautifulSoup(driver.page_source, features="html.parser")
        job_divs = html.findAll("div", attrs={'class': 'job-primary'})

        for div in job_divs:
            detail_link = 'https://www.zhipin.com'
            detail = div.find("div", attrs={'class': 'info-primary'})
            attrs = detail.find("a").attrs
            detail_link = detail_link + attrs["href"] + "?ka=" + attrs["ka"]
            company = div.find("div", attrs={'class': 'company-text'})
            company_name = company.find("a").text
            worker = div.find("div", attrs={'class': 'job-title'}).text
            work_addr = div.find("div", attrs={'class': 'info-primary'}).find("p")
            work_addr = str(work_addr).replace("<p>", "").split("<em class")[0]
            single_info = str(company_name).strip() + "\t" + str(worker).strip() + "\t" + str(
                work_addr).strip() + "\t" + str(detail_link).strip()
            jobs_info.append(single_info)
            print(jobs_info)
            if str(company_name).strip() not in self.uniq_company:
                self.uniq_company_jobs_info.append(single_info)
                self.uniq_company.append(str(company_name))
                with open('files/collection_uniq_company.txt', 'a', encoding='utf-8') as f:
                    f.write(single_info + '\n')
            else:
                print("已搜集过公司名称：" + str(company_name).strip())
                pass

    def get_addr_detail(self):
        for job_info in self.uniq_company_jobs_info:
            detail_link_base = job_info[0:job_info.index('http')]
            detail_link_origin = job_info[job_info.index('http'):len(job_info)]
            self.get_addr_detail_link(detail_link_base, detail_link_origin)

    def get_addr_detail_link(self, detail_link_base, detail_link_origin):
        _link_origin = detail_link_origin
        sleep_second = 15 + random.randint(1, 6)
        print(detail_link_origin + ",等待执行：" + str(sleep_second) + "秒")
        time.sleep(sleep_second)
        try:
            search_header = {
                'User-Agent': user_agent,
            }
            search_proxy = {
                'http': random.choice(main_proxies_http),
                'https': random.choice(main_proxies_https)
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

            # ---    需要修改的代码 -----------------
            addr_detail = job_detail_html.find("div", attrs={'class': 'location-address'})
            if addr_detail:
                addr_detail = addr_detail.text
                if addr_detail:
                    if str(addr_detail).strip():
                        addr_detail_final = str(addr_detail).strip()
                        detail_job_info = str(detail_link_base).strip() + "\t" + addr_detail_final.strip()
                    else:
                        detail_job_info = str(detail_link_base).strip() + "\t" + str(addr_detail).strip()
                else:
                    detail_job_info = str(detail_link_base).strip() + "\t" + "--==--==--"
                detail_job_str = str(detail_job_info).split("\t")
                # print(detail_job_str)
                job_df.append(detail_job_str)
                with open('files/detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
            else:
                detail_job_info = str(detail_link_base).strip() + "\t" + "--==--==--"
                with open('files/detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
        # print(detail_link_origin + ",完成")
        except Exception as get_addr_detail_e:
            print("get_addr_detail 发生异常：" + str(get_addr_detail_e))
            with open("log/collection_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":get_addr_detail 发生异常：" + str(get_addr_detail_e) + '，异常链接：' +
                            str(detail_link_origin) + '\n')
            if 'latin-1' not in str(get_addr_detail_e):
                return self.get_addr_detail_link(detail_link_base, detail_link_origin)
            else:
                if 'gbk' not in str(get_addr_detail_e):
                    return self.get_addr_detail_link(detail_link_base, detail_link_origin)
                else:
                    pass

    def selenuim_quit(self):
        driver.close()

    def selenium_event_input(self, seed_url, input_xpath, input_content, enter_xpath):
        driver.get(seed_url)
        element_input = driver.find_element_by_xpath(input_xpath)
        element_input.send_keys(input_content)
        # element.send_keys(Keys.RETURN)
        # element.click()

    def load_history_data_enhance(self):
        """
        加载历史数据(加强，从详细里面提取已经成功扫描的公诉名称数据)
        :return:
        """
        try:
            root_file = 'files'
            if os.path.exists(root_file):
                root_dirs = os.listdir(root_file)
                if len(root_dirs) > 0:
                    line_uniq = []
                    for file in root_dirs:
                        if 'detail' in file:
                            detail_file = os.path.join(root_file, file)
                            if os.path.isfile(detail_file):
                                with open(detail_file, 'r', encoding='utf-8') as f_his:
                                    if f_his.__sizeof__() > 0:
                                        for line in f_his.readlines():
                                            lines = line.replace('\n', '').split('\t')
                                            if len(lines) > 0:
                                                self.uniq_company.append(lines[0])
            else:
                os.makedirs(root_file)
        except Exception as load_history_data_e:
            with open("log/collection_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":load_history_data 发生异常：" + str(load_history_data_e) + '\n')

            if 'latin-1' not in str(load_history_data_e):
                time.sleep(1)
                raise load_history_data_e
            else:
                if 'gbk' not in str(load_history_data_e):
                    time.sleep(1)
                    raise load_history_data_e
                else:
                    pass

    def detail_to_one(self):
        """
        将所有的detail文件汇总到一个文件中，进行备份和减少空间占用
        :return:
        """
        try:
            root_file = 'files'
            if os.path.exists(root_file):
                root_dirs = os.listdir(root_file)
                if len(root_dirs) > 0:
                    line_uniq = []
                    for file in root_dirs:
                        if 'detail' in file:
                            need_file = os.path.join(root_file, file)
                            if os.path.isfile(need_file):
                                with open(need_file, 'r', encoding='utf-8') as f_his:
                                    for line in f_his.readlines():
                                        if line not in line_uniq:
                                            line_uniq.append(line)

                    # date_time_str_2 = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
                    # with open('files/detail_uniq_company_' + date_time_str_2 + '.txt', 'a',
                    #           encoding='utf-8') as f_new:
                    #     if line_uniq.__len__() > 0:
                    #         for line in line_uniq:
                    #             f_new.write(line)

                    # for file in root_dirs:
                    #     if date_time_str_2 not in file:
                    #         if 'collection_uniq_company' not in file:
                    #             os.remove(os.path.join(root_file, file))

        except Exception as load_history_data_e:
            with open("log/collection_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":load_history_data 发生异常：" + str(load_history_data_e) + '\n')

            if 'latin-1' not in str(load_history_data_e):
                raise load_history_data_e
            else:
                if 'gbk' not in str(load_history_data_e):
                    raise load_history_data_e
                else:
                    pass

    def make_excel(self):
        # print(job_df)
        try:
            data = pd.DataFrame(job_df)
            # 保存数据
            with pd.ExcelWriter('files/collection_' + date_time_str + '.xlsx') as writer:  # doctest: +SKIP
                data.to_excel(writer, sheet_name='51job', index=True, header=0, na_rep='')
            print("生成本期最新的excel表格，文件名为：" + 'files/collection_' + date_time_str + '.xlsx')
        except Exception as make_excel_e:
            with open("log/collection_error.txt", 'a', encoding='utf-8') as f_err:
                f_err.write(date_time_str + ":make_excel 发生异常：" + str(make_excel_e) + '\n')
            if 'latin-1' not in str(make_excel_e):
                raise make_excel_e
            else:
                if 'gbk' not in str(make_excel_e):
                    raise make_excel_e
                else:
                    pass


if __name__ == '__main__':
    selenuimTool = SelenuimTool()
    selenuimTool.load_history_data_enhance()
    # selenuimTool.get_html_source('https://www.zhipin.com')
    # time.sleep(1.5)
    ready_url = 'https://www.zhipin.com'
    selenuimTool.boss_zhipin(ready_url)
    # selenuimTool.get_addr_detail()
    # selenuimTool.make_excel()
