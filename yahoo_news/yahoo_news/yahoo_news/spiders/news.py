import scrapy

from yahoo_news.items import Headline


class NewsSpider(scrapy.Spider):

    name = 'news'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['http://news.yahoo.co.jp/']

    def parse(self, response):
        """ Extract the links to the news topics """

        topic_urls = response.css('section.topics a::attr("href")').re(r'/pickup/\d+$')
        for url in topic_urls:
            yield scrapy.Request(response.urljoin(url), self.parse_topic)

    def parse_topic(self, response):
        """ Extract the title and body on the news page """

        title = response.css('.pickupMain_articleTitle::text').extract_first()
        body = response.css('.pickupMain_articleSummary::text').extract_first()

        yield Headline(title=title, body=body)