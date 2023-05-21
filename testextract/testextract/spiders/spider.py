import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["pds.docs.portworx.com"]
    start_urls = ["https://pds.docs.portworx.com/concepts/overview"]

    main_page=set('/concepts/')

    def parse(self, response):

        links=response.xpath("*//a[@class='mdl-navigation__link']/@href").extract()
        # self.main_page.add(response.xpath("//h1/text()").extract_first())
        main_titles = response.xpath("//*[starts-with(name(), 'h')][following-sibling::p]/text()[not(self::h1)]").getall()
        main_paras = response.xpath("//*[starts-with(name(), 'h')]/following-sibling::p[1]/text()").getall()
        # sub_titles = response.xpath('//h3/text()').getall()

        

        #adds the url of the page and the headings in that page to an output file
        data={
            "url": response.request.url,
            "headings":main_titles,
            "descriptions":main_paras
        }
        yield data

        # visit every left out link in the page
        for link in links:
            if link not in self.main_page:
                self.main_page.add(link)
                base=self.start_urls[0].replace('/concepts','')
                url=base+link
                yield scrapy.Request(url,self.parse)
                

        # print((links))
        # print(main_titles)
        # print(main_paras)
        # print(self.main_page)
    

