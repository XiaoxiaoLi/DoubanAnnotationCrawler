import scrapy
import html2text


class AnnotationSpider(scrapy.Spider):
    name = 'annotation'

    def __init__(self, *args, **kwargs): 
      super(AnnotationSpider, self).__init__(*args, **kwargs) 

      self.start_urls = ['https://book.douban.com/people/{}/annotation/'.format(kwargs.get('username'))] 

    def parse(self, response):
        # follow links to annotation pages
        for href in response.xpath("//div[@class='annotations-context']/h3/a/@href"):
            yield response.follow(href, self.parse_annotation)

        # follow pagination links
        for href in response.css('span.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_annotation(self, response):
        def extract_with_css(selector, query):
            return selector.css(query).extract_first().strip()
        def extract_with_xpath(selector, query):
            return selector.xpath(query).extract_first().strip()
        name = extract_with_css(response, "a.name::text")
        annotations = []
        for sub_annotation in response.xpath('//li[@class="item"]'):
            annotations.append({
                'sub_annotation_title':extract_with_xpath(sub_annotation, './h5/a/text()'),
                'sub_annotation_url': extract_with_xpath(sub_annotation, './h5/a/@href'),
                'content': html2text.html2text(extract_with_xpath(sub_annotation, './pre')),
                'time':extract_with_xpath(sub_annotation,'//div[@class="reply"]/span/text()')
            })
        yield{
            'name': name,
            'subannotations':annotations
        }

