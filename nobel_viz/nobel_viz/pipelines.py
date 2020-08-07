from scrapy.exceptions import DropItem


class DropNonPersons(DropItem):
    """ Drop non person winners """

    def proces_item(self, item, spider):
        if not item['gender']:
            raise DropItem(f"===> NO GENDER FOR {item['name']}")
        return item
