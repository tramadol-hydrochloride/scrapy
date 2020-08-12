from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from tabelog.items import RestaurantItem


class TabelogSpider(CrawlSpider):

    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = ['https://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1']

    rules = [
        # Crawl the pagers (up to page 9, change \d to \d+ for page 10 ~),
        # Then parse the restaurant information page
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
    ]

    def parse_restaurant(self, response):
        """ Parse the restaurant information page """

        # Get lat and lon from the Google Map Image URL
        latitude, longitude = response.css('img.js-map-lazyload::attr("data-original")')\
            .re(r'markers=.*?%7C([\d.]+),([\d.]+)')

        name = response.xpath('//h2[@class="display-name"]/span/text()').extract_first().strip()
        address = response.css('.rstinfo-table__address').xpath('string()').extract_first().strip()
        station = response.xpath('//dt[contains(text(), "最寄り駅")]/following-sibling::dd[1]//span/text()').extract_first()
        score = response.xpath('//span[@class="rdheader-rating__score-val-dtl"]/text()').extract_first()

        yield RestaurantItem(
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
            station=station,
            score=score
        )
