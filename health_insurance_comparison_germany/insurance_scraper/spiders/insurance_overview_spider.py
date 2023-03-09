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

    def start_requests(self):
        urls = [
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=bundesweit&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=11&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=10&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=6&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=7&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=16&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=15&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=9&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=20&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=13&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=8&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=24&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=23&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=12&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=21&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=17&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=18&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=14&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1',
            'https://www.krankenkassen.de/krankenkassen-vergleich/vergleich/?berechnung%5Bberufsgruppe%5D=arbeitnehmer&berechnung%5Bbundesland%5D=19&berechnung%5BmonatlichesBruttoEinkommen%5D=4000&absenden=&berechnung%5Bsortierreihenfolge%5D=&berechnung%5Breferrer%5D=&berechnung%5BempfehlungenAnzeigen%5D=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        nav_page = response.css('div.js-nav-page-wrapper')[0]
        outer_grid = nav_page.css('div.outer-grid').css('div.outer-grid__content.inner-grid.\|.page').css('main')[0]
        frame_link = outer_grid.css('div.page-main__content').css('div.page-main__text iframe::attr(src)')[0].get()
        frame_link = response.urljoin(frame_link)
        yield scrapy.Request(frame_link, callback=self.parse_frame)


    def parse_frame(self, response):
        for block in response.css('div.angebot__tarifdetails.mt-400.sm\:mt-700-n.width-full'):
            provider = block.css('div.fs-450.fw-bolder.lh-200.none.xs\:block.s\:width-5\/12.sm\:width-5\/12.ph-400.sm\:pl-0::text')[0].get()
            for table in block.css('table'):
                for row in table.css('tr'):
                    icon = row.css('td.table__data-icon i::attr(class)').get()
                    if icon == "kk-icon kk-icon-check u-color-signal-green": offered = True
                    elif icon == "kk-icon kk-icon-minus u-color-signal-red": offered = False
                    else: raise ValueError('unknown icon value: ' + icon)

                    yield {
                        'provider': provider,
                        'service': row.css('td.table__data-leistung::text').get(),
                        'offered': offered
                    }

    def parse_download(self, response):
        Path('fullpage.html').write_bytes(response.body)