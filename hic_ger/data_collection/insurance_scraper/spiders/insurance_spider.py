import scrapy


class InsuranceFeeSpider(scrapy.Spider):
    """
    Scrape data about fees and location from german health insurance providers
    """
    name = "fees"

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
                'location': row.css('td::text')[1].get()
            }

        next_page = response.css('div.clearfix.pager a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)