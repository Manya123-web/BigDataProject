# Faculty Finder – Data Engineering Pipeline

An end-to-end **data engineering pipeline** to scrape, clean, analyze, store, and serve faculty profile data from the DA-IICT website via a REST API and a Semantic Search Engine.

The project focuses on **data quality, reproducibility, and clean pipeline design**, utilizing modern NLP techniques for semantic search.

---

## Overview

### Pipeline Flow

```
SCRAPE → CLEAN → ANALYZE → LOAD → EMBED → SERVE
  ↓        ↓        ↓        ↓       ↓      ↓
JSON     CSV   Quality Stats  SQLite  FAISS  FastAPI / Streamlit
```

### Key Features
- **Web Scraping**: robust extraction using Scrapy.
- **Data Cleaning**: normalization and deduplication.
- **Data Quality**: Analysis of missingness and field coverage.
- **Relational Storage**: SQLite for structured data.
- **Semantic Search**: Recommender system using Sentence Transformers & FAISS.
- **Interactive UI**: Streamlit app for exploring faculty and semantic search.
- **REST API**: FastAPI endpoints for data access.

---

## Project Structure

```
BigDataProject/
├── app/
│   ├── main.py              # FastAPI endpoints
│   ├── db.py                # Database connection
│   ├── schemas.py           # Pydantic response models
│   └── static/              # Static assets
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
│   ├── recommender/
│   │   ├── build_index.py   # Generate embeddings & FAISS index
│   │   ├── model.py         # Transformer model loader
│   │   ├── search.py        # Search logic
│   │   └── loader.py        # Startup loader
│   │
│   ├── data/
│   │   ├── raw/             # faculty_output.json
│   │   ├── processed/       # faculty_cleaned.csv
│   │   └── faiss.index      # (Generated) Vector index
│   │
│   └── outputs/
│       └── faculty.db       # SQLite database
│
├── logs/
├── venv/
├── .gitignore
├── requirements.txt
├── streamlit_app.py         # Search & Recommender UI
└── README.md
```

---

## Quick Start

### 1. Setup Environment

```bash
git clone <repo-url>
cd BigDataProject

python -m venv venv
# Activate Virtual Environment:
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
```

---

### 2. Scrape Faculty Data

> **Note**: You must navigate to the scrapy project directory to run the spider.

```bash
cd pipeline/scraping/faculty_finder
scrapy crawl faculty -O ../../../data/raw/faculty_output.json
cd ../../../..  # Return to root for next steps
```

**Output**: `pipeline/data/raw/faculty_output.json`

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

**Output**: `pipeline/data/processed/faculty_cleaned.csv`

---

### 4. Data Quality Analysis (Optional)

```bash
python pipeline/analysis/raw_data_stats.py
python pipeline/analysis/processed_data_stats.py
```

### Key Statistics
**Raw Data (Before Cleaning)**
- Total Records: 112
- Website Links Missing: 56.2%
- Biography Missing: 37.5%

**Processed Data (After Cleaning)**
- Total Records: 112
- Average Record Completeness: 81.2%
- Education Coverage: 98.2%
- Website Links Coverage: 43.8%

> Raw data shows 100% "presence" for many fields because they contain empty strings or placeholders. Processed statistics reflect **actual data usability** after cleaning.



---

### 5. Load Data into Database

```bash
python pipeline/transformation/load_to_db.py
```

**Output**: `pipeline/outputs/faculty.db` (SQLite)

---

### 6. Build Search Index (Recommender)

Generate vector embeddings for semantic search.

```bash
python pipeline/recommender/build_index.py
```


**Output**:
- `pipeline/recommender/data/faiss.index`
- `pipeline/recommender/data/metadata.pkl`

---

### 7. Run Applications

#### **Option A: Streamlit UI (Recommended)**
Interactive interface for search and recommendations.

```bash
streamlit run streamlit_app.py
```
*Access at http://localhost:8501*

#### **Option B: FastAPI Server**
Backend REST API.

```bash
uvicorn app.main:app --reload
```
*Docs at http://127.0.0.1:8000/docs*

---

## API Endpoints

| Endpoint | Description |
|--------|------------|
| `GET /faculty` | Fetch all faculty |
| `GET /faculty/{id}` | Fetch by ID |
| `GET /faculty/name/{name}` | Search by name |
| `GET /faculty/type/{type}` | Filter by type |
| `GET /recommend?query=...` | **Semantic Search** (Vector-based) |
| `GET /faculty/search/keyword/{kw}` | Keyword Search |

---


---

## Technology Stack

- **Scraping**: Scrapy
- **Data Engineering**: Pandas, SQLAlchemy, SQLite
- **API**: FastAPI, Uvicorn, Pydantic
- **ML/Search**: Sentence Transformers (all-mpnet-base-v2), FAISS, Torch
- **Frontend**: Streamlit, HTML/JS injection

---

## Contributors

**Manya Choradiya** (202518022)
GitHub: [Manya123-web](https://github.com/Manya123-web)

**Ambuj Tripathi** (202518021)
GitHub: [Shaneat8](https://github.com/Shaneat8)

---

**Project Type**: Data Engineering & AI
**Focus**: Scraping · Semantic Search · Clean Architecture
