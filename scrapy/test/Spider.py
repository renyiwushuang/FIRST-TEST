# -*- coding: utf-8 -*-
"""
Created on Sat May 05 15:14:15 2018

@author: Administrator
"""

from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
import TorrentItem


class MininovaSpider(CrawlSpider):
    
    name = 'mininova'
    allowed_domains = ['mininova.org']
    start_urls = ['https://www.mininova.org/today']
    rules = [Rule(LinkExtractor(allow =['/tor/\d+']),'parse_torrent')]
    
    def parse_torrent(self,response):
        torrent = TorrentIrem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//h1/text()").extract()
        torrent['descriptioin'] = response.xpath("//div[@id='description']").extract()
        torrent['name'] = response.xpath("//div[@id='specifications']/p[2]/text()").extract()
        return torent