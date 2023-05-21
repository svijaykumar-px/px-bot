import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["pds.docs.portworx.com"]
    start_urls = ["https://pds.docs.portworx.com/concepts/overview/"]

    def parse(self, response):
        # pass
        main_titles = response.xpath("//*[starts-with(name(), 'h')][following-sibling::p]/text()[not(self::h1)]").getall()
        main_paras = response.xpath("//*[starts-with(name(), 'h')]/following-sibling::p[1]/text()").getall()
        # sub_titles = response.xpath('//h3/text()').getall()
        print(main_titles)
        print(main_paras)
        # for title in main_titles:
        #     print(title)

