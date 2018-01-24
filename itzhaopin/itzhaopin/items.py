# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import remove_tags

class TencentItem(Item):
    name = Field()
    catalog = Field()
    workLocation = Field()
    recruitNumber = Field()
    detailLink = Field()
    publishTime = Field()

class LavaJobsItem(Item):
	ID = Field()
	jobdetailLink = Field()
	status = Field()
	priority = Field()
	device = Field()
	#description = Field()
	#submitter = Field()
	#submit_time = Field()
	#end_time = Field()
	#duration = Field()

class SinaRollDocItem(Item):
	title = Field()
	content = Field(
				output_processor = Join()
			)
