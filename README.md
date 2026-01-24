# Faculty Finder

> Web scraping and data processing pipeline for DA-IICT faculty information

## Overview

This project scrapes faculty data from the DA-IICT website, cleans it, and stores it in structured formats (JSON, CSV, SQLite). Built with Scrapy and Python.

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the scraper
cd faculty_finder
python -m scrapy crawl faculty -o faculty_output.json

# Clean the data
cd ..
jupyter notebook data_clean.ipynb
```

## Project Structure

```
BigDataProject/
├── faculty_finder/          # Scrapy project
│   ├── spiders/
│   │   └── faculty_spider.py    # Main scraper
│   └── faculty_output.json      # Scraped data (111 faculty)
├── data_clean.ipynb         # Data cleaning notebook
├── faculty_cleaned.csv      # Cleaned output
└── faculty.db              # SQLite database
```

## Data Collected

| Field | Description |
|-------|-------------|
| name | Full name |
| email | Email addresses |
| phone | Contact numbers (mobile/landline) |
| education | Degrees and institutions |
| specializations | Research areas |
| biography | Professional background |
| teaching | Courses taught |
| publications | Research papers |
| website_links | Google Scholar, personal sites |

## Workflow

1. **Scraping** - Extract data from 5 faculty pages (regular, adjunct, international, distinguished, professor of practice)
2. **Cleaning** - Normalize names, emails, phone numbers, fix encoding issues
3. **Storage** - Save as JSON, CSV, and SQLite database

## Recent Improvements

### Fixed Data Extraction Issues

**Problem**: Missing specializations, publications, and other fields for some faculty members

**Solution**: 
- Updated CSS selectors to match actual HTML structure
- Changed from `div.field--name-field-biography p::text` to `div.field--name-field-biography .field__item *::text`
- Added fallback logic for missing data
- Improved extraction from profile pages

**Result**: Successfully extracting complete data for all 111 faculty members

## Technologies

- **Scrapy** - Web scraping framework
- **Pandas** - Data manipulation
- **Jupyter** - Interactive analysis
- **SQLite** - Database storage

## Data Cleaning Steps

1. **Names** - Convert to title case
2. **Emails** - Replace `[at]` with `@`, `[dot]` with `.`
3. **Phones** - Categorize as mobile or landline
4. **Text** - Remove special characters, normalize whitespace
5. **Publications** - Merge fragmented entries
6. **Links** - Categorize by type (Scholar, LinkedIn, personal)

## Requirements

```
scrapy>=2.14.0
pandas>=2.0.0
jupyter>=1.0.0
```


