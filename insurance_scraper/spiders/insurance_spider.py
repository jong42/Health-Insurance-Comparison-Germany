from pathlib import Path
import scrapy


class InsuranceSpider(scrapy.Spider):
    """
    Scrape data about fees and services from german health insurance providers
    """
    name = "insurance"

    start_urls = [
        'https://www.gkv-spitzenverband.de/service/krankenkassenliste/krankenkassen.jsp',
    ]

    def parse(self, response):
        filename = 'krankenkassenliste.html'
        Path(filename).write_bytes(response.body)
