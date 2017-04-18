import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.cncbinternational.com/personal/investments/securities-trading-service-guide-and-faq/tc/index.jsp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for QnA in response.css('div.JSTaccordionNode'):
            yield {
                'question': QnA.css('div.JSTaccordionHeading li::text').extract(),
                'answer': QnA.css('div.JSTaccordionContent').xpath('string(.)').extract(),


            }
