import scrapy

from hatena.items import WebpageItem
from hatena.utils import get_content


class HatenaSpider(scrapy.Spider):
    name = 'hatena'
    start_urls = [
        'https://b.hatena.ne.jp/entrylist/'
    ]

    def parse(self, response):
        """ Parse Hatena Bookmark new entries page """

        # Crawls the webpage links
        urls = response.xpath('//h3[@class="entrylist-contents-title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)

        # Go to the next page (up to page 5)
        next_page_url = response.xpath('//a/@href').re_first(r'.*\?page=[1-5]')
        if next_page_url:
            # Convert next_page_url (relative path) to an absolute path using urljoin()
            # Request will be processed by parse() without specifying callback
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_page(self, response):
        """ Parse each webpages """

        # Retrieve the title and body by get_content() defined in utils.py
        title, content = get_content(response.text)

        yield WebpageItem(url=response.url, title=title, content=content)
