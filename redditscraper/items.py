# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditscraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    media = scrapy.Field()
    author = scrapy.Field()
    subreddit = scrapy.Field()
    date = scrapy.Field()
    likes = scrapy.Field()
    comments = scrapy.Field()
