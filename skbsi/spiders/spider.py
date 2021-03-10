import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import SkbsiItem
from itemloaders.processors import TakeFirst


class SkbsiSpider(scrapy.Spider):
	name = 'skbsi'
	start_urls = ['https://www.skb.si/sl/aktualno/novice']

	def parse(self, response):
		post_links = response.xpath('//a[@class="link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="years"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="summary"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date"]/text()').get()

		item = ItemLoader(item=SkbsiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
