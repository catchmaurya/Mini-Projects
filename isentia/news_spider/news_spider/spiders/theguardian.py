# -*- coding: utf-8 -*-
import scrapy
from news_spider.items import NewsSpiderItem
import datetime

class TheguardianSpider(scrapy.Spider):
    name = 'theguardian'
    allowed_domains = ['www.theguardian.com']
    start_urls = ['https://www.theguardian.com/au/']

    def parse(self, response):
       # Catergory List is the Article headings of the site
       categoryList = ["headlines","spotlight", "sport", "opinion", "video and pictures", "across the country", "across the world","explore", "the big picture"]
       for i in categoryList:
           # fc-item__container gets the xpath of the article section mentioned in data-title
           sections = response.xpath('//*[@data-title="%s"]//*[@class="fc-item__container"]' % (i) )
           if sections:
               for j in sections:
                   item = NewsSpiderItem()
                   item['article'] = i
                   item['date'] = datetime.datetime.today().strftime("%Y-%m-%d")
                   # keyword can be the short notation of subject/object/comment
                   item['keyword'] = j.xpath('.//*[@class="fc-item__kicker"]/text()').extract_first() or ''
                   # Author name of the article
                   item['author'] = j.xpath('.//*[@class="fc-item__byline"]/text()').extract_first() or ''
                   # headline of the article
                   item['headline']  = j.xpath('.//span[contains(@class,"headline-text")]/text()').extract_first()
                   # URL list of the particular article
                   item['url'] = j.xpath('.//*[@data-link-name="article"]/@href').extract()
                   yield item
                   #print  {'article':i,'author':author, 'keyword':keyword, 'headline':headline,'url':url}
