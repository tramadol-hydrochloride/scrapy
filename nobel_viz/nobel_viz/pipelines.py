import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class NobelImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]

        return item


class DropNonPersons(DropItem):
    """ Drop non person winners """

    def proces_item(self, item, spider):
        if not item['gender']:
            raise DropItem(f"===> NO GENDER FOR {item['name']}")
        return item
