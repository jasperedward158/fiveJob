# -*-coding: utf-8-*-
# https://github.com/chenjiandongx/51job-spider/blob/master/job_spider.py

import os
import time
import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import codecs

import pymongo

class JobSpider:
    '''
    51 job 网站爬虫
    '''

    def __init__(self):
        print("============= initialize =============")
        print("爬取51job 网站Python相关工作")

        self.page_num = 1
        self.next_page = ''
        self.job_keys = u"python"

        self.company = []





    def dataOutput(self, data):
        '''
        写入数据库
        >show dbs
        > use work
        switched to db work
        > db.createCollection('fiveJob')
        > show collections
        fiveJob
        :param data:
        :return:
        '''
        client = pymongo.MongoClient('localhost', 27017)
        db = client.work
        collection = db.fiveJob

        job_id = collection.insert(data)

        print('写入数据：%s' % job_id)



    def htmlParser(self, soup):
        '''
        html parsering
        :param soup:
        :return:
        '''
        formdate = datetime.date.today().strftime("%Y-%m-%d")

        while True:
            infos = soup.find("div", class_="dw_table")
            title = infos.find_all("div", class_="el title")
            elements = infos.find_all("div", class_="el")

            # 获取标题列表
            for t in title:
                title_list = t.text.split('\n')
            h = '-' * 5
            for name in title_list:
                if name != '':
                    h = h + name + '-' * 10

            # 页码
            page = soup.find("div", class_='p_wp')
            # 总页数
            total_page = page.find('span', class_='td').text
            total_page = re.sub('\D', '', total_page)
            # 当前页
            current_page = page.find('li', class_='on').text

            if (int(current_page) == 1 and int(total_page) > 1):
                print(current_page)
                # 跳转下一页的url
                self.next_page = page.find('a', href=True)['href']
                print(self.next_page)

            f = codecs.open(unicode(self.job_keys) + unicode(formdate) + u'.html', 'a+', 'utf-8')

            s1 = '==' * 50 + str(self.page_num) + '==' * 50
            f.write(s1)
            f.write('\r\n')

            f.write(h + '-' * 10 + 'href')
            f.write('\r\n')

            for info in elements:
                a_list = info.find("a")
                if a_list == None:
                    continue

                href = a_list['href']
                post = a_list['title']
                compay = info.find('span', class_='t2').text
                locate = info.find('span', class_='t3').text
                salary = info.find('span', class_='t4').text
                date_time = info.find('span', class_='t5').text

                # 获取职位详情
                self.job_spider(href, isPosition = 1)

                content = unicode(post) + '-' * 10 + unicode(compay) + '-' * 10 + unicode(locate) + '-' * 10 + unicode(
                    salary) + '-' * 5 + unicode(date_time) + '-' * 5 + href

                # 写入文件
                f.write(content)
                f.write('\r\n')

                data = {
                    'post': post,
                    'compay': compay,
                    'locate': locate,
                    'salart': salary,
                    'href': href,
                    'date_time': date_time
                }

                # 写入数据库
                self.dataOutput(data)

            if int(current_page) < int(total_page):
                print(total_page)
                print(self.page_num)

                self.page_num = int(current_page) + 1
                url = self.next_page.split('.html?')
                next_page_url = url[0][0:len(url[0]) - 1] + str(self.page_num) + '.html?' + url[1]

                self.job_spider(next_page_url)
            else:
                break



    def get_position_info(self, dr):
        '''
        职位详情
        :param dr:
        :return:
        '''
        html_const = dr.page_source
        print(html_const)
        #infos = soup.find("div", class_="dw_table")
        break





    def get_job(self, dr, job_keys = '', positions = []):
        '''
        search job
        :param dr: 浏览器
        :param job_keys: 工作关键字
        :param positions 工作地点
        :return:
        '''

        print("job keys %s" % self.job_keys)
        print("the current crawler: %s page" % self.page_num)

        if positions:
            ele_key = dr.find_element_by_id("kwdselectid")
            ele_position = dr.find_element_by_id("work_position_input")
            ele_button = dr.find_element_by_tag_name("button")
            ele_key.clear()
            ele_key.send_keys(job_keys)

            #ele_position.send_keys(u"深圳")
            # search
            # ele_button.click()
            ele_key.send_keys(Keys.ENTER)


        try:
            # 显性等待
            WebDriverWait(dr, 10).until(
                EC.title_contains(unicode(self.job_keys))
            )
        except Exception, e:
            print(e)
            break

        # 强制等待
        time.sleep(5)

        html_const = dr.page_source
        # soup = BeautifulSoup(html_const, 'html.parser', from_encoding='utf-8')
        soup = BeautifulSoup(html_const, 'html.parser')

        # html parsering
        self.htmlParser(soup)





    def job_spider(self, root_url, isPosition = 0, job_key = '', positions = []):
        '''
        爬虫入口
        :param root_url: 目标网站
        :param job_key: 查询关键字
        :param positions 工作地点
        :return:
        '''
        # 驱动浏览器与python对接
        dr = webdriver.Chrome(executable_path=r"/Users/software/chromedriver.exe")
        # 休息50s
        dr.set_page_load_timeout(50)
        # 打开51job首页
        dr.get(root_url)
        # 浏览器窗口最大化
        dr.maximize_window()
        # 控制间隔时间，等待浏览器最大化
        dr.implicitly_wait(10)
        # 找工作
        if isPosition == 1:
            self.get_position_info(dr)
        else:
            if positions:
                self.get_job(dr, job_key, positions)
            else:
                self.get_job(dr)





if __name__ == '__main__':

    spider = JobSpider()

    root_url = 'https://www.51job.com/'
    job_key = u'python'
    positions = [u"北京", u"上海", u"广州", u"深圳"]
    spider.job_spider(root_url, job_key, positions)


