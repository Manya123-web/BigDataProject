# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import sqlite3
import os

class FacultyFinderPipeline:
    def __init__(self):
        self.db_path = "../../../outputs/faculty.db"  # Path relative to spider execution
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty_type TEXT,
                name TEXT,
                education TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                specializations TEXT,
                biography TEXT,
                teaching TEXT,
                research TEXT,
                publications TEXT,
                website_links TEXT,
                image_url TEXT,
                openalex_id TEXT,
                citations INTEGER DEFAULT 0,
                works_count INTEGER DEFAULT 0,
                topics TEXT
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        # Convert lists to strings for storage
        teaching_str = "\n".join(item.get("teaching", []))
        publications_str = "\n".join(item.get("publications", []))
        links_str = "\n".join(item.get("website_links", []))
        
        self.cursor.execute("""
            INSERT INTO faculty (
                faculty_type, name, education, phone, address, email, 
                specializations, biography, teaching, research, 
                publications, website_links, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("faculty_type"),
            item.get("name"),
            item.get("education"),
            item.get("phone"),
            item.get("address"),
            item.get("email"),
            item.get("specializations"),
            item.get("biography"),
            teaching_str,
            item.get("research"),
            publications_str,
            links_str,
            item.get("image_url")
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()
