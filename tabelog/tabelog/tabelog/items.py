import scrapy


class RestaurantItem(scrapy.Item):
    """ Restaurant info on the Tabelog """

    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()