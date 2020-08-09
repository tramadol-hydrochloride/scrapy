import scrapy


class Headline(scrapy.Item):
    """ News headline item. """

    title = scrapy.Field()
    body = scrapy.Field()
