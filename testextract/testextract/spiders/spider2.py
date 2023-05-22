import scrapy
import re

class SpiderSpider(scrapy.Spider):
    name = "spider2"
    allowed_domains = ["docs.portworx.com"]
    start_urls = ['https://pds.docs.portworx.com/concepts/architecture/']
    # start_urls = ['https://baas.docs.portworx.com']
    # start_urls = ["https://pds.docs.portworx.com"]

    # main_page=set('/concepts/')
    main_page=set()
    not_open=['/reference/config-parameters/']

    @staticmethod
    def remove_html_tags(text):
            clean_text = re.sub('<.*?>', '', text)
            clean_text = clean_text.replace('\n','')
            clean_text = re.sub(r'^\s+|\s+$', '', clean_text)
            return clean_text

    def parse(self, response):

        links=response.xpath("*//a[@class='mdl-navigation__link']/@href").extract()
        print(links)
        current_h_tag = None
        p_tags = []
        row_data = ''
    
        for tag in response.css('h1, h2, h3, h4, h5, h6, p, li,tbody, img'):
            if tag.root.tag in ['p','li']:
                p_tags.append(SpiderSpider.remove_html_tags(tag.get()))
            elif tag.root.tag == 'img':
                 p_tags.append(' || IMAGE, PLEASE REFER TO THE LINK || ')

            elif tag.root.tag == 'tbody':
                 td_elements = response.css('tbody tr td')
                 td_data = ' -> '.join(td_elements.xpath('string()').getall())
                 p_tags.append(SpiderSpider.remove_html_tags(td_data))
                 
            else:
                if current_h_tag is not None:
                    # Yield the extracted data when a new h tag is encountered
                    heading = SpiderSpider.remove_html_tags(current_h_tag.get())
                    p_tags = SpiderSpider.remove_html_tags(" ".join(p_tags))

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

        
        # for link in links:
        #         if link not in self.main_page and link.find('config-parameters') == -1:
        #             self.main_page.add(link)
        #             base=self.start_urls[0]
        #             url=base+link
        #             print(url)
        #             yield scrapy.Request(url,self.parse)













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
    

