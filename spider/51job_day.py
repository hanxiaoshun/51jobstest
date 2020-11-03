#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 11:09
# @Author  : Hanxiaoshun@天谕传说
# @Site    : www.shunzi666.cn
# @File    : batch_domain.py
# @Version    : 1.2 强化查询余额操作
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

date_time_str = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))

# ---------------------
jobs_info = []
uniq_company = []
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
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE']

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
        response = self.session.request('GET', url=self.referer, headers=main_header)
        print(response.text)
        print(str(self.session.cookies.get_dict()))
        # self.cookies.set('cookie-name', 'cookie-value', path='/', domain='.abc.com')  # 保存更新cookie
        # self.session.cookies.update()

    def start_spider(self):

        # self.session.cookies['Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a'] = str(math.floor(time.time()))
        # self.session.cookies['_uab_collina'] = boos__uab_collina
        # self.session.cookies['__zp_stoken__'] = boos__zp_stoken__
        # self.session.cookies['__c'] = str(math.floor(time.time()))
        # self.session.cookies['__g'] = boos__g
        # self.session.cookies['__l'] = boos__l
        # self.session.cookies['__l'] = boos__l
        # self.session.cookies['USERAMLOGSIGN'] = USERAMLOGSIGN
        # self.session.cookies['expires'] = str(365)
        print('-----1111------------------------------------')
        # print(str(self.cookies))
        # res = self.session.get('https://www.22.cn/ym/')
        # res.encoding = res.apparent_encoding
        # print(str(res.text))
        # # print(res.content)
        # # self.cookies.update(res.cookies)
        # print(str(self.session.cookies.get_dict()))
        boss_params_search = {
            'lang': 'c',
            'postchannel': '0000',
            'workyear': '99',
            'cotype': '99',
            'degreefrom': '99',
            'jobterm': '99',
            'companysize': '99',
            'ord_field': 0,
            'dibiaoid': 0,
            'line': '',
            'welfare': ''
        }

        search_header = {
            'User-Agent': user_agent,
        }
        # with open('boss_search_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
        #     f.write("最终需要结算的域名: " + final_domains + '\n')
        res = self.session.get(
            'https://search.51job.com/list/040000,000000,0000,00,0,99,%25E5%25A4%2596%25E8%25B4%25B8,2,1.html',
            data=boss_params_search,
            headers=search_header,
            proxies=None,
            timeout=25,
            allow_redirects=True,
            verify=False
        )
        res.encoding = res.apparent_encoding
        print(str(res.text))

        html = BeautifulSoup(res.text, features="html.parser")
        pages = html.find("input", attrs={'id': 'hidTotalPage'}).value
        self.pages = int(pages)

        job_divs = html.findAll("div", attrs={'class': 'el'})
        for div in job_divs:
            if len(div.attrs['class']) == 1:
                company = div.find("span", attrs={'class': 't2'})
                if company:
                    company_name = company.find("a").text
                    company_link = company.find("a").attrs["href"]
                    print(str(company_link).strip())
                    print(str(company_name).strip())
                    worker = div.find("p", attrs={'class': 't1'})
                    worker_name = worker.find("a").text
                    print(str(worker_name).strip())
                    work_addr = div.find("span", attrs={'class': 't3'}).text
                    print(str(work_addr).strip())
                    release_date = div.find("span", attrs={'class': 't5'}).text
                    print(str(release_date).strip())
                    single_info = str(company_name).strip() + "\t" + str(worker_name).strip() + "\t" + str(
                        work_addr).strip() + "\t" + str(release_date).strip() + "\t" + str(company_link).strip()
                    jobs_info.append(single_info)
                    with open('51job_jobs_info_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                        f.write(single_info + "\t" + '\n')
                    if str(company_name).strip() not in uniq_company:
                        uniq_company_jobs_info.append(single_info)
                        with open('51job_jobs_info_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                            f.write(single_info + "\t" + '\n')
                    else:
                        pass
                else:
                    print(div)
            else:
                print(div)

        # print(res.content)
        # self.cookies.update(res.cookies)
        print("res.cookies:::" + str(res.cookies))
        print("res.cookies:::" + str(res.headers))
        print(str(self.session.cookies.get_dict()))

    def next_page(self, page):
        boss_params_search = {
            'lang': 'c',
            'postchannel': '0000',
            'workyear': '99',
            'cotype': '99',
            'degreefrom': '99',
            'jobterm': '99',
            'companysize': '99',
            'ord_field': 0,
            'dibiaoid': 0,
            'line': '',
            'welfare': ''
        }
        search_header = {
            'User-Agent': user_agent,
        }
        # with open('boss_search_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
        #     f.write("最终需要结算的域名: " + final_domains + '\n')
        res = self.session.get(
            'https://search.51job.com/list/040000,000000,0000,00,0,99,%25E5%25A4%2596%25E8%25B4%25B8,2,' + str(
                page) + '.html',
            data=boss_params_search,
            headers=search_header,
            proxies=None,
            timeout=25,
            allow_redirects=True,
            verify=False
        )
        res.encoding = res.apparent_encoding
        print(str(res.text))

        html = BeautifulSoup(res.text, features="html.parser")
        job_divs = html.findAll("div", attrs={'class': 'el'})
        for div in job_divs:
            if len(div.attrs['class']) == 1:
                company = div.find("span", attrs={'class': 't2'})
                if company:
                    company_name = company.find("a").text
                    company_link = company.find("a").attrs["href"]
                    print(str(company_link).strip())
                    print(str(company_name).strip())
                    worker = div.find("p", attrs={'class': 't1'})
                    worker_name = worker.find("a").text
                    print(str(worker_name).strip())
                    work_addr = div.find("span", attrs={'class': 't3'}).text
                    print(str(work_addr).strip())
                    release_date = div.find("span", attrs={'class': 't5'}).text
                    print(str(release_date).strip())
                    single_info = str(company_name).strip() + "\t" + str(worker_name).strip() + "\t" + str(
                        work_addr).strip() + "\t" + str(release_date).strip() + "\t" + str(company_link).strip()
                    jobs_info.append(single_info)
                    with open('51job_jobs_info_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                        f.write(single_info + "\t" + '\n')
                    if str(company_name).strip() not in uniq_company:
                        uniq_company_jobs_info.append(single_info)
                        with open('51job_jobs_info_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                            f.write(single_info + "\t" + '\n')
                        with open('5uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                            f.write(single_info + "\t" + '\n')
                    else:
                        pass

                else:
                    print(div)
            else:
                print(div)

        print("res.cookies:::" + str(res.cookies))
        print("res.cookies:::" + str(res.headers))
        print(str(self.session.cookies.get_dict()))

    def get_addr_detail(self):
        for job_info in uniq_company_jobs_info:
            detail_link_base = job_info[0:job_info.index('http')]
            detail_link_origin = job_info[job_info.index('http'):len(job_info)]
            sleep_second = 2 + random.randint(1, 6)
            print(detail_link_origin + ",等待执行：" + str(sleep_second) + "秒")
            time.sleep(sleep_second)
            # detail_links = str(detail_link_origin).split("?ka=")
            # boss_params_detail = {}
            search_header = {
                'User-Agent': user_agent,
            }
            # with open('boss_search_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
            #     f.write("最终需要结算的域名: " + final_domains + '\n')
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
            print(str(res.text))
            job_detail_html = BeautifulSoup(res.text, features="html.parser")
            if job_detail_html.find("p", attrs={'class': 'fp'}):
                addr_detail = job_detail_html.find("p", attrs={'class': 'fp'}).text
                if addr_detail:
                    if "(邮编" in str(addr_detail).strip():
                        addr_detail_final = str(addr_detail).strip()
                        print(addr_detail_final)
                        addr_detail_final = addr_detail_final[0:addr_detail_final.index('(邮编')]
                        detail_job_info = detail_link_base + "\t" + addr_detail_final.strip() + "\t" + detail_link_origin
                    else:
                        detail_job_info = detail_link_base + "\t" + str(addr_detail).strip() + "\t" + detail_link_origin
                else:
                    detail_job_info = detail_link_base + "\t" + "--==--==--" + "\t" + detail_link_origin
                with open('51job_detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
            else:
                # addr_detail = job_detail_html.find("p", attrs={'class': 'fp'}).text
                # if addr_detail:
                #     detail_job_info = detail_link_base + "\t" + addr_detail + "\t" + detail_link_origin
                # else:
                detail_job_info = detail_link_base + "\t" + "--==--==--" + "\t" + detail_link_origin
                with open('51job_detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f:
                    f.write(detail_job_info + '\n')
            print(detail_link_origin + ",完成")

    def entrance(self):
        try:
            # 与服务器通信握手
            # self.cookie_fetch()
            self.cookie_fetch_get()
            self.start_spider()
            # if self.pages > 1:
            #     for i in range(2, self.pages):
            #         print("第：" + str(i) + "页未采集")
            #         print("等待10秒")
            #         print(str(i))
            #         time.sleep(10 + random.randint(2, 11))
            #         self.next_page(i)
            #         print("第：" + str(i) + "页采集完毕")
            self.get_addr_detail()
            # self.start_verify()
            # self.post_login()
        except Exception as entrance_e:
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
    origin = 'https://www.51job.com/'
    referer = 'https://www.51job.com/'
    # host = 'my.22.cn'
    # accept = 'application/json, text/javascript, */*; q=0.01'
    # verify_URL = "https://my.22.cn/tools/vcode.aspx?codewidth=100&codeheight=25&rand=" + str(random.random())
    # portUrl = "https://my.22.cn/ajax/member/denglu.ashx"
    # login_data = {'username': username,
    #               'pwd': pwd,
    #               'code': 97,
    #               'service': 'my'}
    # spider.verify_URL = verify_URL
    # spider.payloadData = login_data
    spider.origin = origin
    # spider.host = host
    # spider.accept = accept
    spider.referer = referer
    spider.getUrl = 'https://www.51job.com/'
    try:
        spider.entrance()
        end = time.time()
        print('Used time-->', end - start, 's')
    except Exception as e:
        # print(str(e))
        raise e
