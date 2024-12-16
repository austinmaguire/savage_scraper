import scrapy

# Keep running into an AttributeError 
# Installing default reactor before other imports 
from scrapy.utils import reactor 
import asyncio


"""
savagespider is inspired by the book "The Savage Garden" written by
Peter D'Amato the 'Bog Father' of carnivorous plant cultivation.
"""
# TODO: How do we paginate through collections? 
#       When we try to get product elements from collection,
#       link we navigate to shopping cart. JavaScript issue?
# Navigating to first collection page to start

class SavageSpider(scrapy.Spider):
    # the name of the spider
    name = "savagespider"

    allowed_domains = ["californiacarnivores.com"]
    # url of the collection we want to scrape
    start_urls = ["https://www.californiacarnivores.com/collections/sarracenia-hybrids"]
    
    custom_settings = {
            'ROBOTSTXT_OBEY': True,
            'DOWNLOAD_DELAY': 3,
            'COOKIES_ENABLED': False,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def parse(self, response): 
        # Loop through the products - extracting name and price
        products = response.css('a.title')
        for product in products: 
            # return data in format to output 
            yield {
                'name': product.css('::text').get().strip(),
                'price': response.css('span.amount.theme-money::text').get()
            }

        # handle pagination if it exists
        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
