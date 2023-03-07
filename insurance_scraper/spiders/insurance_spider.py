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
        table = response.css('table')[0]
        tbody = table.css('tbody')
        for row in tbody[0].css('tr'):
            yield {
                'name': row.css('a::text').get(),
                'link': row.css('a::attr(href)').get(),
                'fee': row.css('td.alignRight::text').get(),
                'location': row.css('td::text').get()
            }

