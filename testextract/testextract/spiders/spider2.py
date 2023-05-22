import scrapy
import re

class SpiderSpider(scrapy.Spider):
    name = "spider2"
    allowed_domains = ["pds.docs.portworx.com"]
    start_urls = ["https://pds.docs.portworx.com/concepts"]

    main_page=set('/concepts/')

    @staticmethod
    def remove_html_tags(text):
            clean_text = re.sub('<.*?>', '', text)
            clean_text = clean_text.replace('\n','')
            clean_text = re.sub(r'^\s+|\s+$', '', clean_text)
            return clean_text

    def parse(self, response):

        links=response.xpath("*//a[@class='mdl-navigation__link']/@href").extract()
        current_h_tag = None
        p_tags = []

        for tag in response.css('h1, h2, h3, p, tbody'):
            if tag.root.tag == 'p':
                p_tags.append(tag.get())

            # elif tag.root.tag == 'tbody':
            #      rows = tag.css('tr')

            #     # Initialize an empty dictionary to store the key-value pairs
            #      data = {}

            #     # Loop over the table rows and extract the key-value pairs
            #      for row in rows:
            #         key_row = row.css('td:nth-child(1)::text').get().strip()
            #         value_row = row.css('td:nth-child(2)::text').get().strip()

            #         # Store the key-value pair in the dictionary
            #         data[key_row] = value_row

            #     # Yield the scraped data under the respective key
            #      yield {key: data}
            else:
                if current_h_tag is not None:
                    # Yield the extracted data when a new h tag is encountered
                    heading = SpiderSpider.remove_html_tags(current_h_tag.get())
                    p_tags = SpiderSpider.remove_html_tags("".join(p_tags))

                    if len(p_tags)!=0:
              
                        yield {
                            'header': heading,
                            'url': response.request.url,
                            'description': p_tags
                        }
                current_h_tag = tag
                p_tags = []

        # Yield the last set of data after the loop ends
        if current_h_tag is not None:
            heading = SpiderSpider.remove_html_tags(current_h_tag.get())
            p_tags = SpiderSpider.remove_html_tags("".join(p_tags))

            if len(p_tags)!=0:
                         
               yield {
                    'header': heading,
                    'url': response.request.url,
                    'description': p_tags
                }

        
        for link in links:
                if link not in self.main_page:
                    self.main_page.add(link)
                    base=self.start_urls[0].replace('/concepts','')
                    url=base+link
                    yield scrapy.Request(url,self.parse)










        # links=response.xpath("*//a[@class='mdl-navigation__link']/@href").extract()
        # # self.main_page.add(response.xpath("//h1/text()").extract_first())
        # main_titles = response.xpath("//*[starts-with(name(), 'h')][following-sibling::p]/text()[not(self::h1)]").getall()
        # # main_paras = response.xpath("//*[starts-with(name(), 'h')]/following-sibling::p/text()").getall()
        # # sub_titles = response.xpath('//h3/text()').getall()
        # main_paras = response.xpath("//h2/following-sibling::p[following-sibling::h2[1] and preceding-sibling::h2[1]]").getall()

        # # if len(main_titles)==0 and len(main_paras) !=0:
        # #     title=(response.xpath("//h1/text()").extract_first()).replace('\n','')
        # #     title=title.replace(' ','')
        # #     main_titles=[title]

        # print(main_titles)
        # print(main_paras)

        # #adds the url of the page and the headings in that page to an output file
        # data={
        #     "url": response.request.url,
        #     "headings":main_titles,
        #     "descriptions":main_paras
        # }
        # yield data

        #adds heading and description
        # for i in range(len(main_titles)):
        #     if(i < len(main_paras)):
        #         data={
        #             "url":response.request.url,
        #             "heading":main_titles[i],
        #             "description":main_paras[i]
        #         }
        #         yield data


        # visit every left out link in the page
        # for link in links:
        #     if link not in self.main_page:
        #         self.main_page.add(link)
        #         base=self.start_urls[0].replace('/concepts','')
        #         url=base+link
        #         yield scrapy.Request(url,self.parse)
                

        # print((links))
        # print(main_titles)
        # print(main_paras)
        # print(self.main_page)
    

