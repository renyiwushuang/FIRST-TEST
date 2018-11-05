# -*- coding: utf-8 -*-
"""
Created on Sat May 05 15:54:15 2018

@author: Administrator
"""

import scrapy

class NationaldataSpider(scrapy.Spider):
    name = 'Nationaldata'
    allowed_domains = ['http://data.stats.gov.cn']
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A010101&sj=201804',
                  'http://data.stats.gov.cn/search.htm?s=CPI']
    
    def parse(self ,response):
        filename = response.url.split('/')[-2][-2:]+'.html'
        with open(filename,'wb') as f:
            f.write(response.body)