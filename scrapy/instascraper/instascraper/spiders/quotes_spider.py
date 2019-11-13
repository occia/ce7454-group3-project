import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'profiles'
    country = 'canada'
    # Hardcoded path of a country's users names
    file_path = '../../../data/test/usernames/%s.txt' %country
    with open(file_path) as f:
        start_urls = []
        for u in f.readlines():
            start_urls.append('https://imgtagram.com/u/' + u)

    def parse(self, response):
        # Hardcoded name of the country
        country = 'canada'
        for quote in response.css('div.text-block'):
            # The HTML elements we are interested in
            yield {
                'username': quote.css('h3::text').get(),
                'name': quote.css('h1::text').get(),
                'bio': quote.css('p.descp::text').get(),
                'image': response.css('img.icon::attr(src)').get(),
                'country': country
            }