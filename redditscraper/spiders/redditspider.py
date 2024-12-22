import scrapy
from ..items import RedditscraperItem


class RedditspiderSpider(scrapy.Spider):
    name = "redditspider"
    post_count = 0
    urls_count = 0

    def start_requests(self):
        subreddit = ['AmericanHorrorStory']

        for sub in subreddit:
            reddit_search_url = f'https://old.reddit.com/r/{sub}/top/?sort=top&t=week'
            yield scrapy.Request(url=reddit_search_url, callback=self.discover_posts, meta={'subreddit': subreddit})

    def discover_posts(self, response):
        if RedditspiderSpider.urls_count >= 50:
            return

        post_urls = response.css('a.bylink::attr(href)').extract()
        for url in post_urls:
            if RedditspiderSpider.urls_count >= 50:
                break
            RedditspiderSpider.urls_count += 1
            yield scrapy.Request(url=url, callback=self.parse_post_data)

        next_page = response.css('a[rel="nofollow next"]::attr(href)').get()
        if next_page is not None and RedditspiderSpider.urls_count < 50:
            yield scrapy.Request(url=next_page, callback=self.discover_posts)

    def parse_post_data(self, response):
        post_url = response.url
        print("Scraping post: " + post_url)
        print("Post Count: " + str(RedditspiderSpider.post_count))
        post_title = response.css('a.title::text').get()
        post_images = response.css('a img.preview::attr(src)').extract()
        total_text = ''
        texts = response.css('div.usertext.usertext-body p::text').extract()
        for text in texts:
            total_text += text
        post_text = total_text
        post_author = response.css('div.top-matter a.author::text').get()
        post_date = response.css('div.top-matter time::attr(title)').get()
        post_likes = response.css('div.score.unvoted::text')
        if post_likes:
            post_likes = post_likes.get()
        else:
            post_likes = 0
        post_comments = response.css('div.top-matter li.first a.bylink::text')
        if post_comments:
            post_comments = post_comments.get()
            post_comments = post_comments.split()[0]
        else:
            post_comments = 0
        post_subreddit = response.url.split('/')[4]

        item = RedditscraperItem()
        item['url'] = post_url
        item['title'] = post_title
        item['text'] = post_text
        item['media'] = post_images
        item['author'] = post_author
        item['subreddit'] = post_subreddit
        item['date'] = post_date
        item['likes'] = post_likes
        item['comments'] = post_comments

        RedditspiderSpider.post_count += 1
        yield item