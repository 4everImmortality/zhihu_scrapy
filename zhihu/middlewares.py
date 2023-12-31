# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrapy.http.response.html import HtmlResponse


# useful for handling different item types with a single interface


# class seleniumDownloaderMiddleware(object):
#     def __init__(self):
#         options = webdriver.ChromeOptions()
#         # options.add_argument('disable-infobars') #去除警告
#         options.add_argument('headless')  # 无头模式
#         self.driver = webdriver.Chrome(options=options)
#         # self.driver.maximize_window()
#         self.num = 100  # 需要滑滚页面的次数，想拿多一点数据就设置的大一点
#
#     def process_request(self, request, spider):
#         # 第一次请求只需拿到各个板块的url
#         if request.url == 'https://www.zhihu.com/question/399148081':
#             self.driver.get(request.url)
#             time.sleep(1)
#             html = self.driver.page_source
#             response = HtmlResponse(
#                 url=self.driver.current_url,
#                 body=html,
#                 request=request,
#                 encoding="utf-8"
#             )
#             return response
#         else:
#             self.driver.get(request.url)
#             for i in range(self.num):
#                 ActionChains(self.driver).send_keys([Keys.END, Keys.PAGE_UP]).perform()
#                 time.sleep(1)
#             html = self.driver.page_source
#             response = HtmlResponse(
#                 url=self.driver.current_url,
#                 body=html,
#                 request=request,
#                 encoding="utf-8"
#             )
#             return response


class ZhihuSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhihuDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
