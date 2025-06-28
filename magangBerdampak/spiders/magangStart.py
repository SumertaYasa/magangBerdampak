import scrapy


class MagangstartSpider(scrapy.Spider):
    name = "magangStart"
    allowed_domains = ["simbelmawa.kemdikbud.go.id"]
    start_urls = ["https://simbelmawa.kemdikbud.go.id"]

    def parse(self, response):
        pass
