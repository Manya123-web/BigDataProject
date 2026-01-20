from urllib.parse import urlparse
import scrapy
from faculty_finder.items import FacultyFinderItem

class FacultySpider(scrapy.Spider):
    name = "faculty"
    start_urls = [
        "https://www.daiict.ac.in/faculty",
        "https://www.daiict.ac.in/adjunct-faculty",
        "https://www.daiict.ac.in/adjunct-faculty-international",
        "https://www.daiict.ac.in/distinguished-professor",
        "https://www.daiict.ac.in/professor-practice"
                  
                  ]

    def parse(self, response):

        path = urlparse(response.url).path.strip("/")
        faculty_type = path if path else "faculty"

        for faculty in response.css("div.facultyDetails"):
            item = FacultyFinderItem()
            item["faculty_type"] = faculty_type

            item["name"] = faculty.css(
            "h3 a::text"
            ).get(default="").strip()

            item["education"] = faculty.css(
                "div.facultyEducation::text"
            ).get(default="").strip()

            item["phone"] = faculty.css(
                "span.facultyNumber::text"
            ).get(default="").strip()

            item["address"] = faculty.css(
                "span.facultyAddress::text"
            ).get(default="").strip()

            item["email"] = faculty.css(
                "span.facultyemail::text"
            ).get(default="").strip()

            item["specializations"] = faculty.css(
                "div.areaSpecialization p::text"
            ).get(default="").strip()

            # follow profile link
            profile_url = faculty.css(
                "div.personalDetails h3 a::attr(href)"
            ).get()

            if profile_url:
                yield response.follow(
                    profile_url,
                    callback=self.parse_profile,
                    meta={"item": item},
                )
            else:
                yield item

    def parse_profile(self, response):
        item = response.meta["item"]

        # Biography
        item["biography"] = " ".join(
            response.css(
                "div.field--name-field-biography p::text"
            ).getall()
        ).strip()

        # Teaching
        item["teaching"] = response.css(
            "div.field--name-field-teaching li::text"
        ).getall()

        # Publications (ALL – including hidden ones)
        item["publications"] = [
            pub.strip()
            for pub in response.css(
                "div.education ul.bulletText li::text"
            ).getall()
            if pub.strip()
        ]

        # Research (often same as specialization on profile)
        item["research"] = " ".join(
            response.css(
                "div.work-exp p::text"
            ).getall()
        ).strip()

        item["website_links"] = response.css(
            "div.field--name-field-sites a::attr(href)"
        ).getall()
        
        
        yield item