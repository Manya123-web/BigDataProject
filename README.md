# Faculty Finder – Data Engineering Pipeline

An end-to-end **data engineering pipeline** to scrape, clean, analyze, store, and serve faculty profile data from the DA-IICT website via a REST API.

The project focuses on **data quality, reproducibility, and clean pipeline design**, making it suitable for academic evaluation and real-world data engineering use cases.

---

## Overview

### Pipeline Flow

```
SCRAPE → CLEAN → ANALYZE → LOAD → SERVE
  ↓        ↓        ↓        ↓       ↓
JSON     CSV   Quality Stats  SQLite  FastAPI
```

### Key Features
- Web scraping using Scrapy
- Robust data cleaning and normalization
- Raw vs processed data quality analysis
- Relational storage using SQLite
- REST API built with FastAPI

---

## Project Structure

```
BigDataProject/
├── app/
│   ├── main.py              # FastAPI endpoints
│   ├── db.py                # Database connection
│   └── schemas.py           # Pydantic response models
│
├── pipeline/
│   ├── scraping/
│   │   └── faculty_finder/  # Scrapy project
│   │
│   ├── cleaning/
│   │   └── data_clean.py    # Data cleaning logic
│   │
│   ├── transformation/
│   │   └── load_to_db.py    # Load cleaned data into DB
│   │
│   ├── analysis/
│   │   ├── raw_data_stats.py
│   │   └── processed_data_stats.py
│   │
│   ├── data/
│   │   ├── raw/             # faculty_output.json
│   │   └── processed/       # faculty_cleaned.csv
│   │
│   └── outputs/
│       └── faculty.db       # SQLite database
│
├── logs/
├── venv/
├── .gitignore
└── README.md
```

---

## Quick Start

### 1. Setup Environment

```bash
git clone <repo-url>
cd BigDataProject

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install scrapy pandas sqlalchemy fastapi uvicorn pydantic
```

---

### 2. Scrape Faculty Data

```bash
scrapy crawl faculty -O pipeline/data/raw/faculty_output.json
```

**Output**
```
pipeline/data/raw/faculty_output.json
```

---

### 3. Clean Data

```bash
python pipeline/cleaning/data_clean.py
```

**Cleaning Operations**
- Normalize names and text fields
- Convert obfuscated emails to valid format
- Categorize phone numbers (mobile / landline)
- Merge fragmented publication entries
- Normalize empty or invalid values to null

**Output**
```
pipeline/data/processed/faculty_cleaned.csv
```

---

### 4. Data Quality Analysis

```bash
python pipeline/analysis/raw_data_stats.py
python pipeline/analysis/processed_data_stats.py
```

**Purpose**
- Identify hidden missingness in raw data
- Measure true coverage after cleaning
- Evaluate record-level completeness

This step is **read-only** and does not modify data.

---

### 5. Load Data into Database

```bash
python pipeline/transformation/load_to_db.py
```

**Database**
- SQLite database: `pipeline/outputs/faculty.db`
- 111 faculty records
- Semi-structured fields stored as JSON text

---

### 6. Start API Server

```bash
uvicorn app.main:app --reload
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Endpoint | Description |
|--------|------------|
| `GET /faculty` | Fetch all faculty |
| `GET /faculty/{id}` | Fetch faculty by ID |
| `GET /faculty/name/{name}` | Search by name |
| `GET /faculty/type/{type}` | Filter by faculty type |

---

## Example API Response

```json
{
  "id": 1,
  "name": "Yash Vasavada",
  "email": ["yash_vasavada@dau.ac.in"],
  "phone": {
    "landline": ["07968261634"]
  },
  "education": "PhD (EE), Virginia Tech",
  "specializations": "Communication, Signal Processing",
  "faculty_type": "faculty",
  "publications": ["Paper 1", "Paper 2"]
}
```

---

## Data Statistics (Processed)

- Total Records: 111
- Rows with ≥1 missing field: ~67%
- Email Coverage: ~99%
- Phone Coverage: ~68%
- Publication Coverage: ~61%

Raw data shows near-100% field presence due to empty placeholders.  
Processed statistics reflect **actual data usability**.

---

## Technology Stack

- Scrapy – Web scraping
- Pandas – Data cleaning and analysis
- SQLite – Relational storage
- SQLAlchemy – Database abstraction
- FastAPI – REST API framework
- Uvicorn – ASGI server
- Pydantic – Data validation

---

## Future Work

- Semantic search using embeddings (FAISS / ChromaDB)
- Faculty similarity search
- Streamlit or React frontend
- Scheduled scraping and incremental updates

---

## Contributors

**Manya Choradiya** (202518022)  
GitHub: https://github.com/Manya123-web  

**Ambuj Tripathi** (202518021)  
GitHub: https://github.com/Shaneat8  

---

**Project Type**: Data Engineering Pipeline  
**Focus**: Scraping · Data Quality · API Serving
