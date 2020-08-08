import scrapy
import re

from nobel_viz.items import NWinnerItemBio

BASE_URL = 'http://en.wikipedia.org'


class NWinnerSpiderBio(scrapy.Spider):

    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']
    custom_settings = {
        'ITEM_PIPELINES': {'nobel_viz.pipelines.NobelImagesPipeline': 1}
    }

    def parse(self, response):

        file_name = response.url.split('/')[-1]
        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for winner in winners.xpath('li'):
                    winner_data = {}
                    winner_data['link'] = BASE_URL + winner.xpath('a/@href').extract()[0]
                    request = scrapy.Request(winner_data['link'],
                                             callback=self.get_mini_bio)
                    request.meta['item'] = NWinnerItemBio(**winner_data)
                    yield request

    def get_mini_bio(self, response):
        """ Get the winner"s biography and photo """

        BASE_URL_ESCAPED = 'http:\/\/en.wikipedia.org'
        item = response.meta['item']
        item['image_urls'] = []

        img_src = response.xpath('//table[contains(@class,"infobox")]//img/@src')
        if img_src:
            item['image_urls'] = [f'http:{img_src[0].extract()}']

        mini_bio = ''
        paras = response.xpath('//*[@id="mw-content-text"]/div/p[text() or normalize-space(.)=""]').extract()
        for i in range(1, 3):
            mini_bio += paras[i]

        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#', 'href="' + item['link'] + '#')
        item['mini_bio'] = mini_bio

        yield item

