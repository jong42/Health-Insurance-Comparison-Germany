import scrapy
from pathlib import Path


class InsuranceOverviewSpider(scrapy.Spider):
    """
    Scrape data about fees and location from german health insurance providers
    """
    name = "insurance_overview"

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

        next_page = response.css('div.clearfix.pager a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class AokniedersachsenSpider(scrapy.Spider):
    """
    Scrape data about services from AOK Niedersachsen
    """
    name = "AOK_Niedersachsen"

    #start_urls = [
    #    'https://www.aok.de/pk/niedersachsen/',
    #    'http://www.aok.de/hessen',
    #    'http://www.aok.de/baden-wuerttemberg/index.php',
    #    'http: // www.bergische - krankenkasse.de'
    #
    #]

    start_urls = [
    'file:///home/jonas/Desktop/insurance_scraper/Krankenkassen.de.html'
    ]

    def parse(self, response):
        nav_page = response.css('div.js-nav-page-wrapper')[0]
        outer_grid = nav_page.css('div.outer-grid').css('div.outer-grid__content.inner-grid.\|.page').css('main')[0]
        frame_link = outer_grid.css('div.page-main__content').css('div.page-main__text iframe::attr(src)')[0].get()
        yield scrapy.Request(frame_link, callback=self.parse_frame)


    def parse_frame(self, response):
        Path('frame.html').write_bytes(response.body)



#link = response.css('header')[0].css('nav')[0].css('div.relative.overflow-hidden div ul')[0].css('li a::attr(href)')[
#            0].get()
