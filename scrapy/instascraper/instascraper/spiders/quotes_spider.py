import scrapy


class QuotesSpider(scrapy.Spider):
    name = "profiles"

    with open('germany.txt') as f:
        start_urls = f.readlines()

    def parse(self, response):
        for quote in response.css('div.text-block'):
            yield {
                'name': quote.css('h1::text').get(),
                'bio': quote.css('p.descp::text').get(),
                'image': response.css('img.icon::attr(src)').get()
            }

