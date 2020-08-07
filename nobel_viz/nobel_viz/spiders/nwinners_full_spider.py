import scrapy
import re

BASE_URL = 'http://en.wikipedia.org'


class NWinnerSpider(scrapy.Spider):
    """ Scrape the country and link text of the Nobel-winners. """

    name = 'nwinners_full'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    def parse(self, response):

        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for winner in winners.xpath('li'):
                    winner_data = process_winner_li(winner, country[0])
                    request = scrapy.Request(winner_data['link'],
                                             callback=self.parse_bio,
                                             dont_filter=True)
                    request.meta['item'] = NWinnerItem(**winner_data)
                    yield request

    def parse_bio(self, response):

        item = response.meta['item']
        href = response.xpath('//li[@id="t-wikibase"]/a/@href').extract()

        if href:
            request = scrapy.Request(href[0],
                                     callback=self.parse_wikidata,
                                     dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_wikidata(self, response):

        item = response.meta['item']
        property_codes = [
            {'name': 'date_of_birth', 'code': 'P569'},
            {'name': 'date_of_death', 'code': 'P570'},
            {'name': 'place_of_birth', 'code': 'P19', 'link': True},
            {'name': 'place_of_death', 'code': 'P20', 'link': True},
            {'name': 'gender', 'code': 'P21', 'link': True}
        ]

        p_template = '//*[@id="{code}"]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]{link_html}/text()'

        for prop in property_codes:

            link_html = ''
            if prop.get('link'):
                link_html = '/a'
            sel = response.xpath(p_template.format(code=prop['code'], link_html=link_html))
            if sel:
                item[prop['name']] = sel[0].extract()

        yield item


def process_winner_li(winner, country=None):
    """ Process a winner's <li> tag, adding country of birth or nationality. """

    winner_data = {}

    winner_data['link'] = BASE_URL + winner.xpath('a/@href').extract()[0]

    text = ' '.join(winner.xpath('descendant-or-self::text()').extract())

    winner_data['name'] = text.split(',')[0].strip()

    year = re.findall('\d{4}', text)
    if year:
        winner_data['year'] = int(year[0])
    else:
        winner_data['year'] = 0
        print('==> NO YEAR IN ', text)

    category = re.findall('Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics', text)
    if category:
        winner_data['category'] = category[0]
    else:
        winner_data['category'] = ''
        print('==> NO CATEGORY IN ', text)

    if country:
        if text.find('*') != -1:
            winner_data['country'] = ''
            winner_data['born_in'] = country
        else:
            winner_data['country'] = country
            winner_data['born_in'] = ''

    winner_data['text'] = text

    return winner_data
