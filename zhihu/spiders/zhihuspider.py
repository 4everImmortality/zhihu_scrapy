from random import random

import scrapy
from scrapy import Selector
from selenium.common.exceptions import TimeoutException, WebDriverException

from zhihu.items import ZhihuItem
from os import times
from bs4 import BeautifulSoup
import urllib.error
from selenium.webdriver.common.keys import Keys  # 模仿键盘,操作下拉框的
from bs4 import BeautifulSoup  # 解析html的
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from scrapy.exceptions import CloseSpider


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/question/399148081']

    def parse(self, response):
        try:
            html = self.scroll_down()
            # 用xpath提取数据
            sel = Selector(text=html)
            list_items1 = sel.xpath("//div[@class='List-item']")
            list_items2 = sel.xpath("//div[@class='ContentItem AnswerItem']")
            # print(list_items1.text)
            for item1, item2 in zip(list_items1, list_items2):
                zhihu_item = ZhihuItem()
                # 用户名 如果是空的话就是匿名用户
                username = item1.xpath(
                    "div/div[@class='ContentItem AnswerItem']/div[@class='ContentItem-meta']/div[@class='AuthorInfo AnswerItem-authorInfo AnswerItem-authorInfo--related']/div[@class='AuthorInfo']/div[@class='AuthorInfo-content']/div[@class='AuthorInfo-head']/span[@class='UserLink AuthorInfo-name']/div[@class='css-1gomreu']/a[@class='UserLink-link']/text()[1]").extract()
                if not username:
                    username = ['匿名用户']
                print(username)
                # 个人说明
                personalInfo = item1.xpath(
                    "div/div[@class='ContentItem AnswerItem']/div[@class='ContentItem-meta']/div[@class='AuthorInfo AnswerItem-authorInfo AnswerItem-authorInfo--related']/div[@class='AuthorInfo']/div[@class='AuthorInfo-content']/div[@class='AuthorInfo-detail']/div[@class='AuthorInfo-badge']/div[@class='ztext AuthorInfo-badgeText css-14ur8a8']/text()[1]").extract()
                if len(personalInfo) == 0:
                    personalInfo = ['无个人说明']
                # print(personalInfo)
                # 内容
                content = item1.xpath(
                    "div/div[@class='ContentItem AnswerItem']/div[@class='RichContent RichContent--unescapable']/span[1]/div[@class='RichContent-inner']/div/span/p/text()").extract()
                # print(content)
                # 日期
                dateModified = item2.xpath(
                    "div[@class='RichContent RichContent--unescapable']/div[1]/div[@class='ContentItem-time']/a/span/text()[1]").extract()
                # print(dateModified)

                zhihu_item['username'] = username
                zhihu_item['content'] = content
                zhihu_item['dateModified'] = dateModified
                zhihu_item['personalInfo'] = personalInfo
                yield zhihu_item
            time.sleep(0.5)
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Selenium error: {str(e)}")
            raise CloseSpider("Selenium error occurred")
        pass

    def scroll_down(self):
        try:
            # 设置计时器
            start_time = time.time()
            time_limit = 600  # 限制爬虫运行时间为
            # 用selenium模拟浏览器操作
            # 实例化一个浏览器对象
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument('disable-infobars')  # 去除警告
            # 采用请求头伪装
            options.add_argument(
                'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/83.0.4103.116 Safari/537.36"')
            driver = webdriver.Chrome(options=options)
            time.sleep(0.5)
            driver.maximize_window()
            # 访问网页
            driver.get('https://www.zhihu.com/question/399148081')
            # 等待
            time.sleep(random() + 0.5)
            # 点击登录框的x
            driver.find_element(By.XPATH,
                                "/html/body/div[5]/div/div/div/div[2]/button").click()
            # 模拟下拉框
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # 模拟下拉框
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);")
                # 等待加载
                time.sleep(random())
                # 平滑的滚动到页面底部触发js加载
                for i in range(1, 11):
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight - 600 + 550 * {i / 10});")
                    time.sleep(random() / 2 + 0.2)

                time.sleep(random() * 2 + 1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                # 如果新的页面高度和上次的页面高度相同，就退出循环
                if new_height == last_height:
                    break
                if time.time() - start_time > time_limit:
                    break
            # 获取网页源码
            html = driver.page_source
            # 页面爬完或者时间到了就关闭浏览器

            driver.quit()
            # 解析网页源码
            soup = BeautifulSoup(html, 'lxml')
            # print(soup)
            return html
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Selenium error: {str(e)}")
            raise CloseSpider("Selenium error occurred")


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    # 获取当前脚本路径
    dirpath = os.path.dirname(os.path.abspath(__file__))
    # 运行文件绝对路径
    print(os.path.abspath(__file__))
    # 运行文件父路径
    print(dirpath)
    # 添加环境变量
    sys.path.append(dirpath)
    # 切换工作目录
    os.chdir(dirpath)
    # 启动爬虫,第三个参数为爬虫name
    execute(['scrapy', 'crawl', 'zhihuspider'])
