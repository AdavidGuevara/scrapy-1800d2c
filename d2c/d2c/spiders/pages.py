import scrapy


class PagesSpider(scrapy.Spider):
    name = "pages"

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://www.1800d2c.com/all-brands?0dc819aa_page={1}",
            callback= self.parse,
            meta={
                "page_number": 1
            }
        )

    def parse(self, response):
        page_number = response.meta["page_number"]

        urls = response.xpath("//a[contains(@class, 'cardlinkwrap')]/@href").getall()
        for url in urls:
            yield scrapy.Request(
                url="https://www.1800d2c.com" + url,
                callback=self.parse_pages,
            )
        
        if response.css("a.w-pagination-next"):
            yield scrapy.Request(
                url=f"https://www.1800d2c.com/all-brands?0dc819aa_page={page_number + 1}",
                callback= self.parse,
                meta={
                    "page_number": page_number + 1
                }
            )

    def parse_pages(self, response):
        used_tools = response.xpath("//div[contains(@class, 'gridtoolcard')]/a/h2[contains(@class, 'cardheader')]/text()").getall()
        yield {
            "company": response.css("h1.heroh1 ::text").get(),
            "category": response.xpath("//div[contains(@class, 'toolhorizontal')]/a[contains(@class, 'iconlabel')]/div/text()").get(),
            "url": response.css("a.bxl ::attr(href)").extract()[0],
            # "url_d2c": response.url,
            "total_uses_tools": len(used_tools)
        }
