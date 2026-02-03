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
        """
        Main parser - scrapes the faculty listing page
        Gets basic info and follows profile links
        """
        # Get faculty type from URL (like "faculty", "adjunct-faculty", etc)
        path = urlparse(response.url).path.strip("/")
        faculty_type = path if path else "faculty"

        # Loop through each faculty card on the page
        for faculty in response.css("div.facultyDetails"):
            item = FacultyFinderItem()
            item["faculty_type"] = faculty_type

            # Extract basic info from listing page
            item["name"] = faculty.css("h3 a::text").get(default="").strip()
            item["education"] = faculty.css("div.facultyEducation::text").get(default="").strip()
            item["phone"] = faculty.css("span.facultyNumber::text").get(default="").strip()
            item["address"] = faculty.css("span.facultyAddress::text").get(default="").strip()
            item["email"] = faculty.css("span.facultyemail::text").get(default="").strip()
            item["specializations"] = faculty.css("div.areaSpecialization p::text").get(default="").strip()

            # Get profile link - use simpler selector that works for all faculty
            profile_url = faculty.css("h3 a::attr(href)").get()

            if profile_url:
                # Follow the profile link to get detailed info
                yield response.follow(
                    profile_url,
                    callback=self.parse_profile,
                    meta={"item": item},  # Pass the item along
                )
            else:
                # No profile link? Just yield what we have
                yield item

    def parse_profile(self, response):
        """
        Profile page parser - gets detailed info like biography, publications, etc
        """
        # Get the item we passed from parse()
        item = response.meta["item"]

        # === BIOGRAPHY ===
        # Try multiple selectors because website structure varies
        bio_parts = response.css("div.field--name-field-biography *::text").getall()
        if bio_parts:
            item["biography"] = " ".join([t.strip() for t in bio_parts if t.strip()])
        else:
            # Fallback: try simpler selector
            bio_text = response.css("div.field--name-field-biography::text").get(default="").strip()
            item["biography"] = bio_text if bio_text else ""

        # === TEACHING ===
        teaching_list = response.css("div.field--name-field-teaching *::text").getall()
        if teaching_list:
            item["teaching"] = [t.strip() for t in teaching_list if t.strip()]
        else:
            item["teaching"] = []

        # === RESEARCH/SPECIALIZATION ===
        # Check the work-exp div for research areas
        research_parts = response.css("div.work-exp *::text").getall()
        if research_parts:
            research_text = " ".join([t.strip() for t in research_parts if t.strip()])
            item["specializations"] = research_text  # Update with profile page data
            item["research"] = research_text
        else:
            # Keep listing page value if no research found on profile
            item["research"] = item.get("specializations", "")

        # === PUBLICATIONS ===
        # Try multiple selectors
        pubs = []
        
        # Selector 1: div.education.overflowContent
        pubs = [p.strip() for p in response.css("div.education.overflowContent li::text").getall() if p.strip()]
        
        if not pubs:
            # Selector 2: field--name-field-publications
            pubs = [p.strip() for p in response.css("div.field--name-field-publications li::text").getall() if p.strip()]
        
        item["publications"] = pubs

        # === WEBSITE LINKS ===
        # Look for external links in biography or dedicated field
        links = response.css("div.field--name-field-biography a[href*='http']::attr(href)").getall()
        if not links:
            links = response.css("div.field--name-field-sites a::attr(href)").getall()
        
        item["website_links"] = links

        # Log what we extracted (helpful for debugging)
        self.logger.info(f"✓ Extracted profile for: {item.get('name', 'Unknown')}")
        
        yield item