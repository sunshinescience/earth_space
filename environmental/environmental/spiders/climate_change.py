import scrapy
from environmental.items import EnvironmentalItem


class ClimateChangeSpider(scrapy.Spider):
    name = 'climate_change'
    allowed_domains = ["nature.com"]
    
   '''
   start_urls = [
                'https://www.nature.com/nclimate/articles?searchType=journalSearch&sort=PubDate&type=article&page=2'
                ]
    '''
    
    # Obtain next page url to scrape abstracts from that
    # Note that we only assessed abstracts from articles, but other data could be accessed

    start_urls = []
    next_page_href = 'https://www.nature.com/nclimate/articles?searchType=journalSearch&sort=PubDate&type=article&page='
    for num in range(1, 5, 1):
        next_page = next_page_href + str(num)
        start_urls.append(next_page)

    def parse(self, response):
        # Getting individual abstract links from the main page (and calling the parse_abstract function to parse HTML from each link)
        for href in response.xpath('//h3[@class="mb10 extra-tight-line-height word-wrap"]/a/@href').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_abstract)
        
        # Getting the next main page, in order to get more links 
        # next_page = response.xpath('//ol[@class="clean-list pagination pagination-size-5 ma0 grid grid-12 clear"]//li[8]/a/@href').extract_first()
        # next_page_url = response.urljoin(next_page)
        # yield scrapy.Request(next_page_url) # Scrapy uses requests to ask for a page and gets responses from the webserver. 
        
    def parse_abstract(self, response):
        """
        Parse each individual link in order to obtain the abstracts and other information.
        """
        item=EnvironmentalItem()

        item['title'] = response.xpath('//h1[@class="c-article-title u-h1"]/text()').extract_first()
        item['publication_date'] = response.xpath('//li[@class="c-article-identifiers__item"]//time/text()').extract_first()
        item['journal'] = response.xpath('//p[@class="c-article-info-details"]//a/i/text()').extract_first()
        item['article_type'] = response.xpath('//li[@class="c-article-identifiers__item"]/text()').extract_first()
        item['abstract'] = response.xpath('//div[@class="c-article-section__content js-collapsible-section"]//p').extract_first()

        yield item
