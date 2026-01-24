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

        # Biography - using correct Drupal field selector
        biography_text = " ".join(
            response.css(
                "div.field--name-field-biography .field__item *::text"
            ).getall()
        ).strip()
        if biography_text:
            item["biography"] = biography_text
        else:
            item["biography"] = ""

        # Teaching - using correct Drupal field selector
        teaching_list = response.css(
            "div.field--name-field-teaching .field__item *::text"
        ).getall()
        if teaching_list:
            item["teaching"] = [t.strip() for t in teaching_list if t.strip()]
        else:
            item["teaching"] = []

        # Specialization/Research - using the work-exp div after specializationIcon
        specialization_text = " ".join(
            response.css(
                "div.work-exp *::text"
            ).getall()
        ).strip()
        
        # If specialization is found on profile, update it (override listing page value)
        if specialization_text:
            item["specializations"] = specialization_text
            item["research"] = specialization_text
        else:
            # Keep the value from listing page if it exists
            if "research" not in item:
                item["research"] = ""

        # Publications - check multiple possible selectors
        publications = []
        
        # Try first selector: div.education.overflowContent
        pubs_from_education = [
            pub.strip()
            for pub in response.css(
                "div.education.overflowContent li::text"
            ).getall()
            if pub.strip()
        ]
        
        if pubs_from_education:
            publications = pubs_from_education
        else:
            # Try alternative selector
            pubs_from_field = [
                pub.strip()
                for pub in response.css(
                    "div.field--name-field-publications li::text"
                ).getall()
                if pub.strip()
            ]
            publications = pubs_from_field
        
        item["publications"] = publications

        # Website links - look for external links in biography or dedicated field
        website_links = response.css(
            "div.field--name-field-biography a[href*='http']::attr(href)"
        ).getall()
        
        # Also check for any other external links in the profile
        if not website_links:
            website_links = response.css(
                "div.field--name-field-sites a::attr(href)"
            ).getall()
        
        item["website_links"] = website_links
        
        self.logger.info(f"Extracted profile for: {item.get('name', 'Unknown')}")
        
        yield item