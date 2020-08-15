import scrapy


class WebpageItem(scrapy.Item):

    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        """ restrict content length for log not to be too long """

        p = WebpageItem(self)
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'

        return super(WebpageItem, p).__repr__()
