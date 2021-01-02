import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['127.0.0.1']

    # mulai dari urls ini
    # step 1 fokus untuk login
    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        data = {
            "username": "user",
            "password": "user12345"
        }

        return scrapy.FormRequest(
            url="http://127.0.0.1:5000/login",
            formdata=data,
            callback=self.after_login
        )
    # end
    def after_login(self, response):
        yield {"title": response.css("title::text").get()}

