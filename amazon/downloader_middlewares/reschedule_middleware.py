"""
RetryMiddleware
https://github.com/scrapy/scrapy/blob/master/scrapy/downloadermiddlewares/retry.py
DOWNLOADER_MIDDLEWARES = {
    'amazon.downloader_middlewares.reschedule_middleware.ReschedulMiddleware': 800
}
"""
import logging

import scrapy

logger = logging.getLogger(__name__)
class ReschedulMiddleware(object):
    def __init__(self, settings):
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if spider.name != 'basic':
            return response
        magic_word='Chrome'
        new_response = scrapy.http.TextResponse(response.url, body=response.body, encoding='utf-8')
        if magic_word in new_response.text:
            logger.debug("User agent is chrome, maybe try another time, {}".format(response.text))
            return self._retry(request, spider)
        return response

    def _retry(self, request, spider):
        retryreq = request.copy()
        retryreq.dont_filter = True
        retryreq.priority = request.priority + self.priority_adjust
        return retryreq


