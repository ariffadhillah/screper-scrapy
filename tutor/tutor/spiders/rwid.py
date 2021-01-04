from typing import List

import scrapy
from cssselect import Selector


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
        """"
        step ke 2
        1. ambil semua data data barang yang ada di halaman -> akan menuju detail (parsing detail)
        2. ambil semua link next. -> akan balik ke self:after_login

        :param response
        :return
        """

        # get detail produck 1
        detail_products: List[Selector] = response.css(".card .card-title a")
        for detail in detail_products:
            href = detail.attrib.get("href")
            yield response.follow(href, callback=self.parse_detail)

        paginations: List[Selector] = response.css(".pagination a.page-link")
        for pagination in paginations:
            href = pagination.attrib.get("href")
            yield response.follow(href, callback=self.after_login)


    def parse_detail(self, response):
        image = response.css(".card-img-top").attrib.get("src")

        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()

        return {
            "image": image,
            "title": title,
            "stock": stock,
            "desc": description
        }
























