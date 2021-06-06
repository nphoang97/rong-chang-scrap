import scrapy
from scrapy.http.response.html import HtmlResponse

class RongChangeSpider (scrapy.Spider):
    name = "rong_chang"
    #abcdasdf
    def start_requests(self):
        audio_url_pattern = 'https://www.rong-chang.com/usalife/audio/t/usalife{pos}a.mp3'
        content_url_pattern = 'https://www.rong-chang.com/usalife/a/usalife0{pos}a.htm'
        for pos in range(1, 51): 
            url = content_url_pattern.format(pos = self.format_position(pos))
            yield scrapy.Request(url=url, callback=self.parse_content)
    
    def parse_content(self, response):
        self.log("start paragraph")
        text = response.xpath('//p[@class = "timed"]/text()').extract()
        filename = response.url.split('/')[5].split('.')[0] + '.txt'
        self.log("mid" + filename)
        with open(filename, "w") as f:
            f.write(''.join(text))
        f.close()
        self.log("end paragraph")

    def parse_audio(self, response):
        self.log("parse audio")
        filename = response.url.split('/')[6]
        with open(filename, "wb") as f:
            f.write(response.body)
        f.close()
        self.log("save to" + filename)
        self.log("end parse audio")

    def format_position(self, pos):
        if (pos < 10):
            return '0' + str(pos)
        return str (pos)