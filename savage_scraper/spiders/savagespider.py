import scrapy
from scrapy.utils import reactor
import asyncio

class SavageSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping carnivorous plant inventory from California Carnivores website.
    Specifically targets the Sarracenia Hybrids collection. [Plan to scrap future collections, 
    see Known Issues preventing at this time]

    This spider is inspired by "The Savage Garden" by Peter D'Amato - 
    the 'Bog Father' of California Carnivores.

    Attributes:
        name (str): Identifier for the spider
        allowed_domains (list): Restricted domains for crawling
        start_urls (list): Initial URL(s) to begin crawling
        custom_settings (dict): Spider-specific settings including:
            - ROBOTSTXT_OBEY: Respect robots.txt
            - DOWNLOAD_DELAY: Time between requests
            - COOKIES_ENABLED: Cookie handling
            - USER_AGENT: Browser identification
    
    Known Issues:
        - Pagination through collections may fail due to JavaScript rendering
        - Product elements sometimes redirect to shopping cart
    """
    
    name = "savagespider"
    allowed_domains = ["californiacarnivores.com"]
    start_urls = ["https://www.californiacarnivores.com/collections/sarracenia-hybrids"]
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 3,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def clean_text(self, text):
        """
        Clean extracted text by removing extra whitespace and newlines.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: Cleaned text with normalized whitespace
        """
        if text:
            return ' '.join(text.strip().split())
        return None

    def parse(self, response):
        """
        Parse the product listing page and extract product information.
        
        Args:
            response (scrapy.http.Response): The response object containing the page content
            
        Yields:
            dict: Product information containing:
                - name: Name of the plant (or product collection of plants)
                - price: Price of the plant or product
                
        Note:
            Products are extracted from product blocks that contain both name and price
            to ensure correct price mapping. Data cleaning is applied to remove extra
            whitespace and formatting issues.
        """
        # Extract complete product blocks containing both title and price
        product_blocks = response.css('div.product-block__title-price')
        
        for block in product_blocks:
            # Extract name and price from the same block
            name = block.css('a.title::text').get()
            price = block.css('div.price span.amount.theme-money::text').get()
            
            # Clean the extracted data
            clean_name = self.clean_text(name)
            clean_price = self.clean_text(price)
            
            if clean_name and clean_price:
                yield {
                    'name': clean_name,
                    'price': clean_price
                }

        # Handle pagination if available
        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse) 

# Executing with - 
# scrapy crawl savagespider -O savageplants.json