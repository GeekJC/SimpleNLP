import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.cncbinternational.com/personal/investments/securities-trading-service-guide-and-faq/tc/index.jsp',
            'https://www.cncbinternational.com/personal/investments/securities-trading-service-guide-and-faq/en/index.jsp',
            'https://www.cncbinternational.com/personal/investments/securities-trading-service-guide-and-faq/sc/index.jsp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for QnA in response.css('div.JSTaccordionNode'):
            question_no = int(QnA.css('div.JSTaccordionHeading ol::attr(start)').extract_first())
            if question_no <= 18:
                category = response.css('div.cs18 h3::text')[0].extract()
            elif question_no <= 29:
                category = response.css('div.cs18 h3::text')[1].extract()
            elif question_no <= 44:
                category = response.css('div.cs18 h3::text')[2].extract()
            elif question_no <= 53:
                category = response.css('div.cs18 h3::text')[3].extract()
            else:
                category = response.css('div.cs18 h3::text')[4].extract()

            yield {
                'Category': category,
                'Question': QnA.css('div.JSTaccordionHeading li::text').extract(),
                'Answer': QnA.css('div.JSTaccordionContent').xpath('string(.)').extract(),
                'Language': response.url.split("/")[-2]

            }
