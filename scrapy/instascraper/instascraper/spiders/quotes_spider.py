import scrapy

class QuotesSpider(scrapy.Spider):
    name = "profiles"
    country = 'russia'
    file_path = '../../../data/profiles/usernames/%s.txt' %country
    with open(file_path) as f:
        start_urls = f.readlines()

    def parse(self, response):
        country = 'russia'
        for quote in response.css('div.text-block'):
            yield {
                'username': quote.css('h3::text').get(),
                'name': quote.css('h1::text').get(),
                'bio': quote.css('p.descp::text').get(),
                'image': response.css('img.icon::attr(src)').get(),
                'country': country
            }

