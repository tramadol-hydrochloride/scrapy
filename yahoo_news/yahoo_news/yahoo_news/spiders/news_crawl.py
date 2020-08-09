from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from yahoo_news.items import Headline


class NewsCrawlSpider(CrawlSpider):

    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['http://news.yahoo.co.jp/']

    # Rules for how to follow links
    rules = (
        # Crawls to the news page, and process the response by parse_topic()
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topic'),
    )

    def parse_topic(self, response):
        """ Extract the title and body on the news page """

        title = response.css('.pickupMain_articleTitle::text').extract_first()
        body = response.css('.pickupMain_articleSummary::text').extract_first()

        yield Headline(title=title, body=body)


# -------------------------------------
# Examples for how to set a rule
# -------------------------------------

# Crawls to a book page and news page, and process each parse_book() and parse_news()
#
# rules = (
#     Rule(LinkExtractor(allow=r'/book/\w+'), callback='parse_book'),
#     Rule(LinkExtractor(allow=r'/news/\w+'), callback='parse_news'),
# )
#
# Crawls to category page -> product page, then process res by parse_product()
#
# rules = (
#     Rule(LinkExtractor(allow=r'/category/\w+')),
#     Rule(LinkExtractor(allow=r'/product/\w+'), callback='parse_product'),
# )
#
# In the above, process category page by parse_category()
#
# rules = (
#     Rule(LinkExtractor(allow=r'/category/\w+'), callback='parse_category', follow=True),
#     Rule(LinkExtractor(allow=r'/product/\w+'), callback='parse_product'),
# )
