# Faculty Finder

A complete data engineering pipeline that scrapes, cleans, stores, and serves faculty information from the DA-IICT website through a REST API.

---

## Table of Contents

- [Project Overview](#project-overview)
- [What This Project Does](#what-this-project-does)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Understanding the Pipeline](#understanding-the-pipeline)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Data Dictionary](#data-dictionary)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

This project demonstrates a complete data engineering workflow:

1. Web scraping faculty data from DA-IICT website
2. Cleaning and transforming messy HTML data
3. Storing structured data in SQLite database
4. Serving data through FastAPI endpoints

**Target Audience**: Beginner data scientists who want to understand how raw web data becomes a production-ready API.

**Final Goal**: Enable semantic search where users can query "Who works on sustainable energy?" and find relevant faculty members.

**Current Stage**: Data engineering pipeline (Project 1 of 2)

---

## What This Project Does

Imagine you want to find all professors working on "machine learning" at your college. Instead of manually browsing faculty pages, this system:

1. Automatically visits each faculty member's profile page
2. Extracts their name, email, research interests, publications, etc.
3. Cleans the data (fixes encoding issues, organizes phone numbers)
4. Stores everything in a database
5. Provides an API so you can query: `GET /faculty/type/faculty`

**Real-world use case**: A student portal that shows "Top 5 faculty in AI research" or "Contact information for IoT experts."

---

## Technologies Used

| Tool             | Purpose          | Why This Tool?                                                                               |
| ---------------- | ---------------- | -------------------------------------------------------------------------------------------- |
| Scrapy           | Web scraping     | Industry-standard framework for crawling and extracting structured web data                  |
| Pandas           | Data cleaning    | Powerful and flexible library for transforming and validating messy datasets                 |
| SQLite           | Database         | Lightweight, serverless database ideal for learning and prototyping                          |
| SQLAlchemy       | Database ORM     | Provides a Pythonic, database-agnostic way to interact with SQLite and manage queries safely |
| FastAPI          | REST API         | Modern Python framework with high performance and auto-generated OpenAPI documentation       |
| Pydantic         | Data validation  | Ensures type-safe API responses and enforces data consistency using Python type hints        |
| Uvicorn          | ASGI server      | Lightweight, high-performance server used to run FastAPI applications                        |
| Jupyter Notebook | Data exploration | Interactive environment for testing and validating data cleaning logic                       |

---

## Project Structure


```
BigDataProject/
│
├── faculty_finder/              # Scrapy project folder
│   ├── spiders/
│   │   └── faculty_spider.py    # Main web scraper
│   ├── items.py                 # Items to be crawlled
│   └── faculty_output.json      # Raw scraped data (111 faculty members)
│
├── app/                         # FastAPI application
│   ├── main.py                  # API routes and logic
│   ├── db.py                    # Database connection setup
│   └── schemas.py               # Data validation models
│
├── data_clean.ipynb             # Jupyter notebook for data cleaning
├── faculty_cleaned.csv          # Cleaned data in CSV format
├── faculty.db                   # SQLite database (final structured data)
├── requirements.txt             # Python dependencies
├── logs/
│   └── llm_usage.md             # Detailed log of ChatGPT assistance
└── README.md                    # This file
```

---

## Setup Instructions

### Prerequisites

Before starting, ensure you have the following installed on your system:

#### 1. Python Installation

**Check if Python is installed**:
```bash
python --version
# Should show Python 3.8 or higher
```

**If not installed**:

**Windows**:
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify: Open Command Prompt and type `python --version`

**Mac**:
```bash
# Using Homebrew (install Homebrew first from brew.sh)
brew install python@3.11
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### 2. Git Installation

**Check if Git is installed**:
```bash
git --version
```

**If not installed**:
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
- **Mac**: `brew install git`
- **Linux**: `sudo apt install git`

#### 3. Code Editor (Recommended)

**VS Code** (Beginner-friendly):
- Download from [code.visualstudio.com](https://code.visualstudio.com/)
- Install Python extension (search "Python" in Extensions)

**Alternative**: PyCharm, Sublime Text, or any text editor

#### 4. Verify pip Installation

```bash
pip --version
# or
pip3 --version
```

If pip is not installed:
```bash
# Windows/Mac/Linux
python -m ensurepip --upgrade
```

### Step-by-Step Setup

#### Step 1: Clone the Repository

```bash
# Navigate to where you want the project
cd Desktop  # or any folder you prefer

# Clone the repository
git clone <your-repo-url>

# Enter the project folder
cd BigDataProject
```

**If you don't have Git**, download the ZIP file from GitHub and extract it.

#### Step 2: Create Virtual Environment

**Why virtual environment?** Keeps project dependencies isolated from other Python projects.

```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

**Activate the virtual environment**:

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

**You should see `(venv)` prefix in your terminal**:
```
(venv) C:\Users\YourName\Desktop\BigDataProject>
```

#### Step 3: Install Required Packages

**Option A: Install from requirements.txt** (Recommended)

```bash
pip install -r requirements.txt
```

**Option B: Install packages individually**

```bash
pip install scrapy==2.11.0
pip install pandas==2.1.0
pip install jupyter==1.0.0
pip install fastapi==0.104.0
pip install uvicorn==0.24.0
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0
```

**Verify installation**:
```bash
pip list
# Should show all installed packages
```

#### Step 4: Verify Scrapy Installation

```bash
scrapy version
# Should output Scrapy version number
```

#### Step 5: Test Jupyter Notebook

```bash
jupyter notebook
# Should open browser with Jupyter interface
```

Press `Ctrl+C` in terminal to stop Jupyter.

### Create requirements.txt File

If you don't have a `requirements.txt` file, create one:

**File: `requirements.txt`**
```
scrapy==2.11.0
pandas==2.1.0
jupyter==1.0.0
notebook==7.0.6
fastapi==0.104.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
```

### Troubleshooting Installation

#### Issue: "pip is not recognized"

**Solution**:
```bash
# Use Python module syntax
python -m pip install <package_name>
```

#### Issue: "Permission denied" (Mac/Linux)

**Solution**:
```bash
# Use --user flag
pip install --user <package_name>
```

#### Issue: Scrapy installation fails on Windows

**Solution**: Install Microsoft C++ Build Tools
1. Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install "Desktop development with C++"
3. Retry: `pip install scrapy`

#### Issue: Cannot activate virtual environment on Windows

**Solution**: Run PowerShell as Administrator
```powershell
Set-ExecutionPolicy RemoteSigned
```

Then retry activation.

---

## How to Run

### Step 1: Scrape Faculty Data

```bash
cd faculty_finder
python -m scrapy crawl faculty -o faculty_output.json
```

**What happens**: Scrapy visits DA-IICT faculty pages and extracts 111 faculty profiles into `faculty_output.json`.

**Expected output**: A JSON file with raw faculty data (may contain encoding issues, inconsistent formats).

### Step 2: Clean the Data

```bash
cd ..
jupyter notebook data_clean.ipynb
```

**What happens**: 
- Opens Jupyter notebook in your browser
- Run all cells (Cell → Run All)
- Produces `faculty_cleaned.csv` and `faculty.db`

**What gets cleaned**:
- Names converted to title case
- Emails formatted properly (replacing `[at]` with `@`)
- Phone numbers categorized as mobile/landline
- Publications merged into complete entries
- Website links categorized by type

### Step 3: Start the API

```bash
uvicorn app.main:app --reload
```

**What happens**: API server starts at `http://127.0.0.1:8000`

**Access documentation**: Open browser and visit `http://127.0.0.1:8000/docs`

### 3. Database Storage Code

**File Location**: `data_clean.ipynb` (continued)

#### Convert Complex Data to JSON Strings

```python
# Define which columns contain lists/dictionaries
JSON_COLUMNS = [
    "phone",           # Dictionary: {"mobile": [...], "landline": [...]}
    "email",           # List: ["email1@...", "email2@..."]
    "teaching",        # List: ["Course 1", "Course 2"]
    "publications",    # List: ["Publication 1", "Publication 2"]
    "website_links"    # Dictionary: {"google_scholar": [...], "linkedin": [...]}
]
```

**Why this is necessary**:
- SQLite doesn't have native list or dictionary types
- Must convert Python objects → JSON strings for storage
- When reading back, convert JSON strings → Python objects

```python
def to_json_safe(value):
    """
    Converts lists/dicts to JSON strings for SQLite storage.
    """
    
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    
    return None if pd.isna(value) else value
```

**Explanation Line-by-Line**:

```python
if isinstance(value, (list, dict)):
```
- `isinstance(value, (list, dict))`: Checks if value is list OR dict
- Tuple `(list, dict)` = check multiple types
- Example values:
  - List: `["course1", "course2"]` → True
  - Dict: `{"mobile": ["123"]}` → True
  - String: `"text"` → False

```python
    return json.dumps(value, ensure_ascii=False)
```
- `json.dumps()`: Convert Python object → JSON string
  - `dumps` = "dump string" (serialize to string)
- `ensure_ascii=False`: Keep Unicode characters as-is
  - Without this: `{"name": "José"}` → `{"name": "Jos\\u00e9"}`
  - With this: `{"name": "José"}` → `{"name": "José"}`

**Example transformations**:
```python
Input: {"mobile": ["9876543210"], "landline": ["0796826"]}
Output: '{"mobile": ["9876543210"], "landline": ["0796826"]}'  # String now!

Input: ["Course 1", "Course 2", "Course 3"]
Output: '["Course 1", "Course 2", "Course 3"]'  # String now!
```

```python
    return None if pd.isna(value) else value
```
- `pd.isna(value)`: Checks if value is NaN (Not a Number = missing)
- For non-list/dict values, keep them as-is (unless NaN)

**Apply to JSON columns**:
```python
for col in JSON_COLUMNS:
    df[col] = df[col].apply(to_json_safe)
```

**Explanation**:
- Loop through each column name
- Apply conversion function to entire column
- Now phone, email, etc. are JSON strings

**Verify data types after conversion**:
```python
from collections import defaultdict

column_types = defaultdict(set)

for col in df.columns:
    for val in df[col]:
        if val is not None:
            column_types[col].add(type(val).__name__)

column_types
```

**Output example**:
```python
{
    'name': {'str'},
    'email': {'str'},      # Now string (JSON), was list
    'phone': {'str'},      # Now string (JSON), was dict
    'education': {'str'},
    ...
}
```

#### Create SQLite Database Schema

```python
import sqlite3

# Connect to database (creates file if doesn't exist)
conn = sqlite3.connect("faculty.db")
cursor = conn.cursor()
```

**Explanation**:
- `sqlite3.connect()`: Opens connection to database file
- If `faculty.db` doesn't exist, creates it
- `cursor`: Object to execute SQL commands
  - Think of cursor as a "pointer" to database

```python
try:
    # Drop existing table if it exists (fresh start)
    cursor.execute("DROP TABLE IF EXISTS faculty")
```

**Explanation**:
- `DROP TABLE`: Deletes table and all its data
- `IF EXISTS`: Don't error if table doesn't exist
- Why do this? Ensures we start with clean schema

```python
    # Create table with schema
    cursor.execute("""
    CREATE TABLE faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_type TEXT,
        name TEXT,
        education TEXT,
        address TEXT,
        specializations TEXT,
        biography TEXT,
        research TEXT,
        phone TEXT,
        email TEXT,
        teaching TEXT,
        publications TEXT,
        website_links TEXT
    )
    """)
```

**Explanation - SQL Syntax**:

```sql
CREATE TABLE faculty (
```
- `CREATE TABLE`: SQL command to create new table
- `faculty`: Table name

```sql
    id INTEGER PRIMARY KEY AUTOINCREMENT,
```
- `id`: Column name
- `INTEGER`: Data type (whole numbers: 1, 2, 3...)
- `PRIMARY KEY`: Unique identifier for each row
  - No two rows can have same ID
  - Used to reference specific faculty member
- `AUTOINCREMENT`: Database automatically assigns next number
  - First row: id = 1
  - Second row: id = 2
  - You don't manually set it

```sql
    faculty_type TEXT,
```
- `TEXT`: Stores text/strings
- SQLite data types:
  - `INTEGER`: Whole numbers
  - `REAL`: Decimal numbers
  - `TEXT`: Strings
  - `BLOB`: Binary data
  - `NULL`: No value

```sql
    phone TEXT,
    email TEXT,
```
- Why TEXT for phone/email?
  - They're stored as JSON strings now
  - Example: `'{"mobile": ["9876543210"]}'`

**Why TEXT for everything except ID?**
- Simple and flexible
- JSON strings can represent complex structures
- Easier to parse in Python
- No need for multiple tables with relationships

```python
    conn.commit()  # Save changes to database
    conn.close()   # Close connection
```

**Explanation**:
- `commit()`: Saves all changes permanently
  - Without this, changes are lost when connection closes
  - Like clicking "Save" in a document
- `close()`: Closes database connection
  - Frees up system resources

```python
except Exception as e:
    print(f"Error creating database table: {e}")
```

**Explanation**:
- Catches any errors during table creation
- `Exception as e`: Stores error details in variable `e`
- `f"..."`: F-string for string formatting

#### Insert Data into Database

**First, add ID column to DataFrame**:

```python
df = df.reset_index(drop=True)  # Reset row numbers
df.insert(0, "id", range(1, len(df) + 1))  # Add ID column
```

**Explanation**:
- `reset_index(drop=True)`: Resets row numbers to 0, 1, 2...
  - `drop=True`: Don't keep old index as column
- `df.insert(position, column_name, values)`: Adds new column
  - `0`: Insert at first position (leftmost)
  - `"id"`: Column name
  - `range(1, len(df) + 1)`: Generates numbers 1, 2, 3, ..., 111
    - `len(df)` = 111 (total rows)
    - `range(1, 112)` = 1 to 111 (112 is exclusive)

**Insert using SQLAlchemy** (recommended method):

```python
try:
    from sqlalchemy import create_engine
    
    # Create database engine
    engine = create_engine("sqlite:///faculty.db")
```

**Explanation**:
- SQLAlchemy: Higher-level database library
  - Easier than raw SQL
  - Handles data types automatically
- `create_engine()`: Creates connection to database
- `"sqlite:///faculty.db"`: Connection string
  - `sqlite:///`: Protocol for SQLite
  - `faculty.db`: Database filename
  - Three slashes `///`: Relative path (same folder)
  - For absolute path: `"sqlite:////full/path/to/faculty.db"`

```python
    df.to_sql(
        "faculty",              # Table name
        con=engine,             # Database connection
        if_exists="replace",    # What to do if table exists
        index=False             # Don't write DataFrame index
    )
```

**Explanation**:
- `.to_sql()`: Pandas method to write DataFrame → SQL table
- `"faculty"`: Table name in database
- `con=engine`: Which database to use
- `if_exists="replace"`: Options:
  - `"replace"`: Delete old table, create new one
  - `"append"`: Add to existing table
  - `"fail"`: Error if table exists (default)
- `index=False`: Don't include DataFrame row numbers
  - We already have `id` column

**What happens behind the scenes**:
```python
# For each row in DataFrame, SQLAlchemy generates SQL:
INSERT INTO faculty (id, faculty_type, name, education, ...)
VALUES (1, 'faculty', 'Yash Vasavada', 'PhD (EE), Virginia Tech', ...);

INSERT INTO faculty (id, faculty_type, name, education, ...)
VALUES (2, 'faculty', 'Yash Agrawal', 'PhD (ECE), NIT Hamirpur', ...);

# ... and so on for all 111 rows
```

```python
    print("Data inserted into faculty.db successfully.")
except Exception as e:
    print(f"Error inserting data into database: {e}")
```

#### Verify Data in Database

```python
try:
    # Connect to database
    conn = sqlite3.connect("faculty.db")
    
    # Query first 3 rows
    result = pd.read_sql(
        "SELECT * FROM faculty LIMIT 3",
        conn
    )
    
    print(result)
    conn.close()
```

**Explanation**:
- `pd.read_sql()`: Execute SQL query, return DataFrame
- SQL query breakdown:
  - `SELECT *`: Get all columns
  - `FROM faculty`: From this table
  - `LIMIT 3`: Only first 3 rows
- Result is a DataFrame you can inspect

**Expected output**:
```
   id faculty_type          name  ...
0   1      faculty  Yash Vasavada  ...
1   2      faculty   Yash Agrawal  ...
2   3      faculty Vinay Palaparthy ...
```

```python
except Exception as e:
    print(f"Error querying database: {e}")
```

---

### 4. FastAPI Application Code

**File Structure**:
```
app/
├── main.py       # API routes and logic
├── db.py         # Database connection
└── schemas.py    # Data validation models
```

#### File 1: Database Connection (db.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
```

**What are these?**
- `create_engine`: Creates database connection
- `sessionmaker`: Factory for creating database sessions
- **Session**: Manages conversation with database
  - Open session → Query → Close session

```python
# Database URL (relative path)
DATABASE_URL = "sqlite:///faculty.db"
```

**Explanation**:
- Relative to where you run `uvicorn` command
- If you run from project root, looks for `faculty.db` there

```python
# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

**Explanation**:
- `create_engine()`: Establishes connection to database
- `connect_args`: Additional parameters for SQLite
- `{"check_same_thread": False}`: 
  - SQLite default: Can only be used in thread that created it
  - FastAPI is multi-threaded (handles multiple requests simultaneously)
  - This setting: Allow access from any thread
  - **Important for web applications**

```python
# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

**Explanation**:
- `SessionLocal`: Factory (creates new sessions on demand)
- `autocommit=False`: Don't automatically save changes
  - We control when to commit (manual save)
- `autoflush=False`: Don't automatically sync changes to database
  - More control over when data is written
- `bind=engine`: Connect sessions to our database engine

```python
def get_db():
    """
    Dependency function that provides database session to routes.
    Automatically closes session after request completes.
    """
    db = SessionLocal()  # Create new session
    try:
        yield db         # Provide session to route
    finally:
        db.close()       # Always close, even if error
```

**Explanation - Why use yield?**
- `yield`: Pauses function, returns value, resumes later
- Flow:
  1. Create session (`db = SessionLocal()`)
  2. Give session to route handler (`yield db`)
  3. Route handler uses session
  4. Return to this function
  5. Clean up (`db.close()`)

**Without yield (wrong)**:
```python
def get_db():
    db = SessionLocal()
    return db  # Route gets session, but who closes it?
```

**With yield (correct)**:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db  # Route uses session
    finally:
        db.close()  # Guaranteed cleanup
```

**Real-world analogy**:
- Like checking out a library book (session)
- `yield`: Lend book to reader
- `finally`: Book returned automatically when done

#### File 2: Data Models (schemas.py)

```python
from pydantic import BaseModel
from typing import Optional, List, Dict
```

**What is Pydantic?**
- Data validation library
- Ensures API responses match expected structure
- Auto-generates documentation
- Type checking at runtime

```python
class FacultyOut(BaseModel):
    """
    Defines structure of faculty data returned by API.
    Pydantic validates that responses match this structure.
    """
    
    id: int
```

**Explanation**:
- `id: int`: Must be an integer
- If you try to return string, Pydantic throws error
- Type hints provide:
  - Documentation (auto-generated)
  - Validation (catches errors)
  - IDE autocomplete

```python
    faculty_type: Optional[str]
    name: Optional[str]
    education: Optional[str]
    address: Optional[str]
    specializations: Optional[str]
    biography: Optional[str]
    research: Optional[str]
```

**Explanation**:
- `Optional[str]`: Can be string OR None
- Equivalent to: `Union[str, None]`
- Without `Optional`: Field is required
- With `Optional`: Field can be missing

```python
    phone: Optional[Dict[str, List[str]]]
```

**Explanation - Complex Type**:
- `Dict[str, List[str]]`: Dictionary where:
  - Keys are strings
  - Values are lists of strings
- Example:
  ```python
  {
      "mobile": ["9876543210", "9123456789"],
      "landline": ["07968261634"]
  }
  ```
- Breakdown:
  - `Dict`: Python dictionary
  - `[str, ...]`: Key type is string
  - `[..., List[str]]`: Value type is list of strings

```python
    email: Optional[List[str]]
```

**Explanation**:
- `List[str]`: List containing only strings
- Example: `["email1@dau.ac.in", "email2@dau.ac.in"]`

```python
    teaching: Optional[List[str]]
    publications: Optional[List[str]]
```

**Explanation**:
- Same pattern: Lists of strings

```python
    website_links: Optional[Dict[str, List[str]]]
```

**Explanation**:
- Same complex type as phone
- Example:
  ```python
  {
      "google_scholar": ["https://scholar.google.com/..."],
      "linkedin": ["https://linkedin.com/in/..."],
      "personal_website": ["https://example.com"]
  }
  ```

```python
    class Config:
        orm_mode = True
```

**Explanation**:
- `Config`: Pydantic configuration
- `orm_mode = True`: Enables reading from ORM objects
  - ORM = Object-Relational Mapping (SQLAlchemy)
  - Allows: SQLAlchemy row → Pydantic model
- Without this:
  - Must convert SQLAlchemy object → dict → Pydantic model
- With this:
  - Direct conversion: SQLAlchemy object → Pydantic model

#### File 3: API Routes (main.py)

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import json

from app.db import get_db
from app.schemas import FacultyOut
```

**Import Breakdown**:
- `FastAPI`: Main application class
- `Depends`: Dependency injection (automatic parameter providing)
- `HTTPException`: For error responses (404, 500, etc.)
- `RedirectResponse`: Redirect users to different URL
- `Session`: Type hint for database session
- `text`: Write raw SQL queries
- `List`: Type hint for lists
- `json`: Parse JSON strings
- `get_db`: Our database session provider (from db.py)
- `FacultyOut`: Response model (from schemas.py)

```python
# Create FastAPI application
app = FastAPI(title="Faculty API")
```

**Explanation**:
- `FastAPI()`: Creates application instance
- `title="Faculty API"`: Shown in auto-generated docs
- `app`: Variable name (convention)

```python
# Define which fields are stored as JSON strings in database
JSON_FIELDS = {
    "phone",
    "email",
    "teaching",
    "publications",
    "website_links",
}
```

**Explanation**:
- Set of field names
- Used for parsing: JSON string → Python object
- Set `{}` vs List `[]`:
  - Set: Fast lookup (`if field in JSON_FIELDS`)
  - No duplicates
  - Order doesn't matter

```python
def parse_row(row: dict) -> dict:
    """
    Converts database row to dictionary with parsed JSON fields.
    Transforms JSON strings back to Python lists/dicts.
    """
    
    # Convert SQLAlchemy Row to regular dict
    data = dict(row)
```

**Explanation**:
- `row: dict`: Type hint (input is dict-like)
- `-> dict`: Type hint (output is dict)
- `dict(row)`: SQLAlchemy Row → Python dictionary
- SQLAlchemy Row object has special methods, converting to dict makes it easier to work with

```python
    # Parse each JSON field
    for field in JSON_FIELDS:
        value = data.get(field)
```

**Explanation**:
- Loop through field names: `"phone"`, `"email"`, etc.
- `.get(field)`: Gets value of that field from dictionary
  - `data.get("phone")` → `'{"mobile": ["9876543210"]}'`
  - `.get()` returns `None` if key doesn't exist (safe)

```python
        if value is None:
            data[field] = None
```

**Explanation**:
- If field is NULL in database, keep as None
- Don't try to parse None (would cause error)

```python
        else:
            try:
                data[field] = json.loads(value)
```

**Explanation**:
- `json.loads()`: Convert JSON string → Python object
  - `loads` = "load string" (deserialize from string)
- Examples:
  ```python
  '["email@dau.ac.in"]' → ["email@dau.ac.in"]  # String to list
  
  '{"mobile": ["9876"]}' → {"mobile": ["9876"]}  # String to dict
  ```

```python
            except Exception:
                data[field] = None
```

**Explanation**:
- If JSON parsing fails (malformed JSON), set to None
- Prevents entire API request from failing
- Better to return `None` than crash

```python
    return data
```

#### API Route 1: Get All Faculty

```python
@app.get("/faculty", response_model=List[FacultyOut])
def get_all_faculty(db: Session = Depends(get_db)):
```

**Explanation - Decorator**:
- `@app.get("/faculty")`: HTTP GET request to `/faculty` endpoint
  - Full URL: `http://127.0.0.1:8000/faculty`
- `response_model=List[FacultyOut]`: Response is list of faculty objects
  - Enables validation and auto-documentation

**Explanation - Function Parameters**:
- `db: Session = Depends(get_db)`: Dependency injection
  - `db`: Variable name for database session
  - `Session`: Type hint
  - `Depends(get_db)`: FastAPI calls `get_db()`, provides result as `db`
- **How it works**:
  1. User makes request to `/faculty`
  2. FastAPI sees `Depends(get_db)`
  3. Calls `get_db()` function
  4. `get_db()` yields database session
  5. FastAPI passes session as `db` parameter
  6. After function completes, `get_db()` closes session

```python
    # Execute SQL query
    result = db.execute(text("SELECT * FROM faculty"))
```

**Explanation**:
- `db.execute()`: Run SQL query
- `text("...")`: Wrap raw SQL in text() for SQLAlchemy
- `SELECT * FROM faculty`: Get all columns, all rows

```python
    rows = result.mappings().all()
```

**Explanation**:
- `result`: Query result object (not actual data yet)
- `.mappings()`: Convert rows to dictionary-like objects
  - Each row becomes: `{"id": 1, "name": "John", ...}`
- `.all()`: Fetch ALL results into memory
  - Returns list of row objects

**Why `.mappings()` is IMPORTANT**:
- Without: Rows are tuples `(1, "John", "john@email", ...)`
  - Must access by index: `row[0]`, `row[1]`
- With: Rows are dict-like `{"id": 1, "name": "John", ...}`
  - Access by name: `row["id"]`, `row["name"]`

```python
    return [parse_row(row) for row in rows]
```

**Explanation**:
- List comprehension: Process each row
- `parse_row(row)`: Convert JSON strings → Python objects
- Returns list of dictionaries
- FastAPI automatically:
  1. Validates against `FacultyOut` model
  2. Converts to JSON
  3. Sends to user

#### API Route 2: Get Faculty by ID

```python
@app.get("/faculty/{faculty_id}", response_model=FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
```

**Explanation**:
- `"/faculty/{faculty_id}"`: URL pattern with variable
  - `{faculty_id}`: Placeholder
  - Example URLs: `/faculty/1`, `/faculty/25`, `/faculty/111`
- `faculty_id: int`: Path parameter
  - FastAPI extracts from URL
  - Automatically converts to integer
  - If user visits `/faculty/abc`, FastAPI returns error (not an int)

```python
    result = db.execute(
        text("SELECT * FROM faculty WHERE id = :id"),
        {"id": faculty_id}
    )
```

**Explanation - Parameterized Query**:
- `WHERE id = :id`: SQL with placeholder `:id`
- `{"id": faculty_id}`: Parameters dictionary
  - Replaces `:id` with actual value
- **Why not f-string?** Prevents SQL injection!

**Bad (SQL Injection vulnerable)**:
```python
query = f"SELECT * FROM faculty WHERE id = {faculty_id}"
# If faculty_id = "1 OR 1=1", selects ALL rows!
```

**Good (Safe)**:
```python
query = text("SELECT * FROM faculty WHERE id = :id")
params = {"id": faculty_id}
# SQLAlchemy properly escapes value
```

```python
    row = result.mappings().first()
```

**Explanation**:
- `.first()`: Get first (and only) result
  - Returns single row object OR None
- Different from `.all()` which returns list

```python
    if not row:
        raise HTTPException(status_code=404, detail="Faculty not found")
```

**Explanation**:
- If query returns no results, `row` is `None`
- `HTTPException`: FastAPI's error class
- `status_code=404`: HTTP "Not Found" status
- `detail`: Error message returned to user
- Stops function execution, returns error response

```python
    return parse_row(row)
```

**Explanation**:
- Parse the single row
- FastAPI validates against `FacultyOut`
- Returns JSON object (not array)

#### API Route 3: Search by Name

```python
@app.get("/faculty/name/{faculty_name}", response_model=List[FacultyOut])
def get_by_name(faculty_name: str, db: Session = Depends(get_db)):
```

**Explanation**:
- `faculty_name: str`: Path parameter (string type)
- Example URL: `/faculty/name/yash`

```python
    result = db.execute(
        text("""
            SELECT * FROM faculty
            WHERE LOWER(name) LIKE LOWER(:name)
        """),
        {"name": f"%{faculty_name}%"}
    )
```

**Explanation - SQL Breakdown**:
- `LOWER(name)`: Convert name to lowercase
  - `"Yash Vasavada"` → `"yash vasavada"`
- `LIKE`: Pattern matching
- `LOWER(:name)`: Convert search term to lowercase
- `%{faculty_name}%`: Wildcard pattern
  - `%`: Matches any characters (0 or more)
  - `%yash%`: Matches anything containing "yash"
    - Matches: "Yash Vasavada", "Yash Agrawal", "Ayash Kumar"

**Example**:
```python
# User searches for "yash"
# Becomes: LOWER(name) LIKE LOWER('%yash%')
# Matches:
#   - "Yash Vasavada" (starts with)
#   - "Yash Agrawal" (starts with)
#   - "Ayash Kumar" (contains in middle)
```

```python
    rows = result.mappings().all()
    return [parse_row(row) for row in rows]
```

**Explanation**:
- Returns all matching faculty
- Could be 0, 1, or many results

#### API Route 4: Filter by Faculty Type

```python
@app.get("/faculty/type/{faculty_type}", response_model=List[FacultyOut])
def get_by_type(
    faculty_type: FacultyType,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("SELECT * FROM faculty WHERE faculty_type = :t"),
        {"t": faculty_type.value}
    )
    rows = result.mappings().all()
    return [parse_row(row) for row in rows]
```

**Explanation**:
- Uses an Enum (FacultyType) to restrict input to a predefined set of valid faculty types
- Exact match on faculty_type (no LIKE used)
- Prevents invalid values at the API level and provides a dropdown in Swagger UI
- Example URL: /faculty/type/adjunct-faculty
- Returns all faculty records belonging to the selected faculty type


#### API Route 5: Root Redirect

```python
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
```

**Explanation**:
- When user visits `http://127.0.0.1:8000/`
- Automatically redirects to `http://127.0.0.1:8000/docs`
- `include_in_schema=False`: Don't show in API documentation
- `RedirectResponse`: HTTP 307 redirect
- Improves user experience (no blank page)

---

### Running the Complete System

#### Step 1: Start the API Server

```bash
# Make sure you're in project root directory
cd BigDataProject

# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server
uvicorn app.main:app --reload
```

**Command Breakdown**:
- `uvicorn`: ASGI server (runs FastAPI apps)
- `app.main`: Python module path
  - `app`: Folder name
  - `main`: File name (`main.py`)
- `:app`: Variable name in `main.py`
  - From: `app = FastAPI(...)`
- `--reload`: Auto-restart when code changes (development mode)

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Step 2: Access API Documentation

Open browser and visit:
```
http://127.0.0.1:8000/docs
```

You'll see interactive API documentation where you can:
- View all endpoints
- See request/response schemas
- Test endpoints directly in browser
- No need for Postman or curl!

#### Step 3: Test Endpoints

**In the browser documentation**:
1. Click endpoint (e.g., `GET /faculty`)
2. Click "Try it out"
3. Click "Execute"
4. See response below

**Using curl** (command line):
```bash
# Get all faculty
curl http://127.0.0.1:8000/faculty

# Get faculty by ID
curl http://127.0.0.1:8000/faculty/1

# Search by name
curl http://127.0.0.1:8000/faculty/name/yash

# Filter by type
curl http://127.0.0.1:8000/faculty/type/faculty
```

**Using Python**:
```python
import requests

# Get all faculty
response = requests.get("http://127.0.0.1:8000/faculty")
faculty = response.json()  # List of faculty objects

# Get specific faculty
response = requests.get("http://127.0.0.1:8000/faculty/1")
person = response.json()  # Single faculty object
print(person["name"])  # Access name field
```

---

## Understanding the Pipeline

### 1. Web Scraping Code (faculty_spider.py)

**File Location**: `faculty_finder/spiders/faculty_spider.py`

#### Complete Spider Code with Explanations

```python
import scrapy

class FacultySpider(scrapy.Spider):
    # Spider name - used to run: scrapy crawl faculty
    name = 'faculty'
    
    # List of URLs to start scraping
    start_urls = [
        'https://www.daiict.ac.in/faculty',           # Regular faculty
        'https://www.daiict.ac.in/faculty-adjunct',    # Adjunct faculty
        'https://www.daiict.ac.in/faculty-international',  # International
        'https://www.daiict.ac.in/faculty-distinguished',  # Distinguished
        'https://www.daiict.ac.in/faculty-professor-practice'  # Professor of practice
    ]
```

**Explanation**:
- `scrapy.Spider`: Base class provided by Scrapy framework
- `name = 'faculty'`: Identifier for this spider (used in commands)
- `start_urls`: List of pages to begin crawling from
- **Why multiple URLs?** Faculty are categorized on different pages

```python
    def parse(self, response):
        """
        This method is automatically called for each URL in start_urls.
        It processes the faculty listing page and extracts profile links.
        """
        
        # Extract the category from URL
        # Example: 'https://www.daiict.ac.in/faculty' → 'faculty'
        faculty_type = response.url.split('/')[-1]
```

**Explanation**:
- `parse()`: Default callback method called by Scrapy
- `response`: Contains the downloaded webpage
- `response.url`: Current page URL
- `.split('/')[-1]`: Takes last part after final slash
  - Example: `'https://www.daiict.ac.in/faculty'` → splits into `['https:', '', 'www.daiict.ac.in', 'faculty']` → takes `'faculty'`

```python
        # Find all faculty profile links on the page
        # CSS selector targets <a> tags inside faculty card containers
        faculty_links = response.css('div.views-row a::attr(href)').getall()
```

**Explanation**:
- `response.css()`: Query webpage using CSS selector
- `div.views-row`: Targets `<div class="views-row">` elements
- `a::attr(href)`: Gets the `href` attribute from `<a>` tags
- `.getall()`: Returns list of ALL matching elements
  - Alternative: `.get()` returns only the first match

**HTML Structure It's Targeting**:
```html
<div class="views-row">
    <a href="/faculty/dr-john-doe">Dr. John Doe</a>
</div>
<div class="views-row">
    <a href="/faculty/dr-jane-smith">Dr. Jane Smith</a>
</div>
```

```python
        # Visit each faculty member's profile page
        for link in faculty_links:
            # response.follow() handles relative URLs automatically
            # callback=self.parse_faculty tells Scrapy which method to use
            yield response.follow(
                link, 
                callback=self.parse_faculty,
                meta={'faculty_type': faculty_type}  # Pass category to next page
            )
```

**Explanation**:
- `for link in faculty_links`: Iterate through each profile URL
- `response.follow()`: Creates new request to visit that URL
  - Handles relative URLs: `/faculty/dr-john` → `https://www.daiict.ac.in/faculty/dr-john`
- `callback=self.parse_faculty`: Function to process the profile page
- `meta={'faculty_type': ...}`: Pass data between requests
- `yield`: Returns the request to Scrapy's scheduler (doesn't block execution)

```python
    def parse_faculty(self, response):
        """
        Extracts detailed information from individual faculty profile page.
        This method is called for each faculty member's page.
        """
        
        # Retrieve the category passed from previous page
        faculty_type = response.meta.get('faculty_type')
```

**Explanation**:
- `response.meta.get('faculty_type')`: Retrieves data passed from `parse()` method
- `.get()` method returns `None` if key doesn't exist (safe access)

```python
        # Extract faculty name from page title
        # CSS selector: h1.page-title → <h1 class="page-title">Dr. John Doe</h1>
        # ::text → gets the text content inside the tag
        # .get() → returns first match (there's only one page title)
        # .strip() → removes leading/trailing whitespace
        name = response.css('h1.page-title::text').get()
        if name:
            name = name.strip()
```

**Explanation**:
- `h1.page-title::text`: CSS pseudo-element to extract text
- `.get()`: Returns single value (or None if not found)
- `.strip()`: Removes `" Dr. John Doe "` → `"Dr. John Doe"`
- `if name:`: Only strip if name exists (prevents error on None)

```python
        # Extract education information
        # Multiple selectors provide fallback if first one fails
        education = (
            response.css('div.field--name-field-education .field__item *::text').getall() or
            response.css('div.field--name-field-education::text').getall()
        )
        education = ' '.join(education).strip() if education else None
```

**Explanation**:
- `or` operator: Try first selector, if empty try second
- `.getall()`: Returns list of all matching text nodes
- `*::text`: Captures text from all nested elements
  ```html
  <div class="field__item">
      <p>PhD from <strong>MIT</strong></p>
  </div>
  ```
  Result: `['PhD from ', 'MIT']`
- `' '.join(education)`: Combines list into single string
  - `['PhD from ', 'MIT']` → `'PhD from MIT'`
- `if education else None`: Returns None if list is empty

```python
        # Extract phone numbers
        phone = response.css('div.field--name-field-phone .field__item::text').get()
        if phone:
            phone = phone.strip()
```

**Explanation**:
- `.field__item::text`: Gets text directly inside the div (not nested elements)
- Result might be: `"079-68261634, 9882114669"`
- Cleaning happens later in data_clean.ipynb

```python
        # Extract office address
        address = response.css('div.field--name-field-address .field__item::text').getall()
        address = ' '.join(address).strip() if address else None
```

**Explanation**:
- Same pattern as education extraction
- Joins multiple lines into single address string

```python
        # Extract email addresses
        email = response.css('div.field--name-field-email .field__item::text').getall()
        email = ', '.join(email).strip() if email else None
```

**Explanation**:
- `.join()` with `', '`: Separates multiple emails with comma
- Result: `"john@dau.ac.in, john.doe@gmail.com"`

```python
        # Extract research specializations
        specializations = response.css(
            'div.field--name-field-specializations .field__item *::text'
        ).getall()
        specializations = ' '.join(specializations).strip() if specializations else None
```

**Explanation**:
- `*::text`: Crucial for nested content
- Example HTML:
  ```html
  <div class="field__item">
      <span>Machine Learning</span>, <span>AI</span>
  </div>
  ```
- Without `*`: Would miss text inside `<span>` tags
- With `*`: Captures all text: `['Machine Learning', ', ', 'AI']`

```python
        # Extract biography/professional background
        biography = response.css(
            'div.field--name-field-biography .field__item *::text'
        ).getall()
        biography = ' '.join(biography).strip() if biography else None
```

**Explanation**:
- Biography often contains formatted text with paragraphs, bold, italics
- `*::text` captures all text regardless of HTML formatting

```python
        # Extract teaching information (courses taught)
        teaching = response.css(
            'div.field--name-field-teaching .field__item li::text'
        ).getall()
        if not teaching:
            teaching = response.css(
                'div.field--name-field-teaching .field__item *::text'
            ).getall()
        teaching = [t.strip() for t in teaching if t.strip()] if teaching else None
```

**Explanation**:
- First try `li::text`: Assumes courses are in `<li>` list items
  ```html
  <ul>
      <li>Data Structures</li>
      <li>Algorithms</li>
  </ul>
  ```
- If no `<li>` found, fallback to all text
- List comprehension: `[t.strip() for t in teaching if t.strip()]`
  - Strips whitespace from each item
  - Filters out empty strings
  - `if t.strip()`: Only include non-empty items

```python
        # Extract research interests
        research = response.css(
            'div.field--name-field-research .field__item *::text'
        ).getall()
        research = ' '.join(research).strip() if research else None
```

**Explanation**:
- Similar to biography extraction
- Joins all text into single string

```python
        # Extract publications
        publications = response.css(
            'div.field--name-field-publications .field__item li::text'
        ).getall()
        if not publications:
            publications = response.css(
                'div.field--name-field-publications .field__item *::text'
            ).getall()
        publications = [p.strip() for p in publications if p.strip()] if publications else None
```

**Explanation**:
- Publications might be in lists or paragraphs
- Two-step extraction ensures we catch both formats
- Stores as list (not joined) because each publication is separate item

```python
        # Extract website links (Google Scholar, personal website, etc.)
        website_links = response.css(
            'div.field--name-field-website a::attr(href)'
        ).getall()
```

**Explanation**:
- `a::attr(href)`: Extracts URL from `href` attribute
- Example HTML:
  ```html
  <div class="field--name-field-website">
      <a href="https://scholar.google.com/...">Google Scholar</a>
      <a href="https://personal-site.com">Website</a>
  </div>
  ```
- Result: `['https://scholar.google.com/...', 'https://personal-site.com']`

```python
        # Create dictionary with all extracted data
        # yield returns this data to Scrapy
        yield {
            'faculty_type': faculty_type,
            'name': name,
            'education': education,
            'phone': phone,
            'address': address,
            'email': email,
            'specializations': specializations,
            'biography': biography,
            'teaching': teaching,
            'research': research,
            'publications': publications,
            'website_links': website_links
        }
```

**Explanation**:
- `yield`: Returns data to Scrapy without stopping function
- Dictionary structure: Key-value pairs
- Data is saved to JSON file specified in command: `-o faculty_output.json`
- Each `yield` creates one JSON object in the output file

#### Why Use yield Instead of return?

```python
# yield allows processing multiple items
def parse(self, response):
    for link in faculty_links:
        yield response.follow(link, ...)  # Doesn't stop, continues loop
        
# return would stop after first item
def parse(self, response):
    for link in faculty_links:
        return response.follow(link, ...)  # Stops immediately!
```

#### Running the Spider

```bash
cd faculty_finder
python -m scrapy crawl faculty -o faculty_output.json
```

**Command breakdown**:
- `python -m scrapy`: Run Scrapy as Python module
- `crawl faculty`: Use spider named "faculty"
- `-o faculty_output.json`: Output to JSON file
  - `-o`: Output flag
  - Creates/overwrites the file

**Alternative formats**:
```bash
# CSV format
scrapy crawl faculty -o output.csv

# JSON Lines format (one JSON object per line)
scrapy crawl faculty -o output.jsonl
```

---

### Stage 1: Web Scraping (Ingestion)

**File**: `faculty_finder/spiders/faculty_spider.py`

**Challenge**: Faculty data is spread across multiple pages with inconsistent HTML structure.

**Solution**:
```python
# The spider visits 5 different faculty category pages
start_urls = [
    'https://www.daiict.ac.in/faculty',
    'https://www.daiict.ac.in/faculty-adjunct',
    # ... more URLs
]

# For each faculty member, it extracts:
yield {
    'name': ...,
    'email': ...,
    'education': ...,
    # ... more fields
}
```

**Key learning**: CSS selectors target specific HTML elements. Example: `h1.page-title::text` extracts the faculty name from `<h1 class="page-title">Dr. John Doe</h1>`.

### 2. Data Cleaning Code (data_clean.ipynb)

**File Location**: `data_clean.ipynb` (Jupyter Notebook)

#### Import Required Libraries

```python
import pandas as pd      # Data manipulation
import json             # JSON parsing/serialization
import re               # Regular expressions for pattern matching
import unicodedata      # Unicode normalization (fix encoding issues)
```

**What each library does**:
- **pandas**: Excel-like data manipulation (think of it as Python's Excel)
- **json**: Convert Python objects ↔ JSON strings
- **re**: Pattern matching (find phone numbers, emails)
- **unicodedata**: Fix garbled characters like `â€œ`

#### Load Scraped Data

```python
# Read JSON file into pandas DataFrame
df = pd.read_json("faculty_finder/faculty_output.json")
print(f"Data loaded: {len(df)} rows")
```

**Explanation**:
- `pd.read_json()`: Reads JSON file into table-like structure
- `df`: Short for DataFrame (standard variable name)
- `len(df)`: Number of rows (faculty members)

**DataFrame structure**:
```
     name              email                   phone
0    Yash Vasavada     yash[at]dau[dot]...    079-68261634
1    Yash Agrawal      yash_agrawal[at]...    079-68261629, 9882114669
```

#### Function 1: Clean Faculty Names

```python
def title_case_name(name):
    """
    Converts names to title case (First Letter Capitalized).
    Example: 'JOHN DOE' → 'John Doe', 'jane smith' → 'Jane Smith'
    """
    
    # Check if name is valid string
    if not isinstance(name, str) or name.strip() == "":
        return None
    
    # Convert to title case
    return name.title()
```

**Explanation Line-by-Line**:

```python
if not isinstance(name, str) or name.strip() == "":
```
- `isinstance(name, str)`: Checks if variable is a string (not number, None, etc.)
- `not isinstance(...)`: Inverts the check (True if NOT a string)
- `name.strip() == ""`: Checks if string is empty or only whitespace
  - `"  ".strip()` → `""` (empty)
- `or`: If EITHER condition is True, return None

```python
return name.title()
```
- `.title()`: Built-in Python method
- Capitalizes first letter of each word
- Examples:
  - `"YASH VASAVADA"` → `"Yash Vasavada"`
  - `"yash vasavada"` → `"Yash Vasavada"`
  - `"yAsH vAsAvAdA"` → `"Yash Vasavada"`

**Apply to entire column**:
```python
df['name'] = df['name'].apply(title_case_name)
```

**Explanation**:
- `df['name']`: Selects the 'name' column
- `.apply(function)`: Runs function on EVERY row in that column
- Overwrites original column with cleaned values

#### Function 2: Clean Email Addresses

```python
def clean_email(email):
    """
    Converts email from obfuscated format to standard format.
    Example: 'yash[at]dau[dot]ac[dot]in' → 'yash@dau.ac.in'
    """
    
    # Check if email is valid and non-empty
    if not isinstance(email, str) or not email.strip():
        return None
```

**Explanation**:
- `not email.strip()`: True if string is empty or only whitespace
  - `"   ".strip()` → `""` → `not ""` → `True`

```python
    # Replace obfuscated characters
    email = email.replace("[at]", "@").replace("[dot]", ".")
```

**Explanation**:
- `.replace(old, new)`: Substitutes all occurrences
- Chained calls: First replace `[at]`, then replace `[dot]`
- Example transformation:
  ```
  'yash[at]dau[dot]ac[dot]in'
  → 'yash@dau[dot]ac[dot]in'  (after first replace)
  → 'yash@dau.ac.in'          (after second replace)
  ```

```python
    # Remove any spaces
    email = email.replace(" ", "")
```

**Explanation**:
- Handles cases like `"yash @dau. ac. in"` → `"yash@dau.ac.in"`

```python
    # Split multiple emails by comma
    emails = [e for e in email.split(",") if "@" in e]
```

**Explanation - Step by Step**:

1. `email.split(",")`: Splits string by commas
   - `"yash@dau.ac.in, john@dau.ac.in"` → `["yash@dau.ac.in", " john@dau.ac.in"]`

2. `for e in email.split(",")`: Loops through each email

3. `if "@" in e`: Only includes strings containing `@`
   - Filters out invalid entries like `""` or `"not-an-email"`

4. `[... for ...]`: List comprehension (compact for-loop)
   - Creates new list with filtered results

**Equivalent long form**:
```python
emails = []
for e in email.split(","):
    if "@" in e:
        emails.append(e)
```

```python
    # Return list of emails or None if empty
    return emails if emails else None
```

**Explanation**:
- `emails if emails else None`: Ternary operator
- If `emails` list is not empty, return it
- If `emails` list is empty `[]`, return `None`
- Examples:
  - `["a@b.com"]` → returns `["a@b.com"]`
  - `[]` → returns `None`

**Apply to column**:
```python
df['email'] = df['email'].apply(clean_email)
```

#### Function 3: Clean General Text

```python
def clean_text(text):
    """
    Fixes encoding issues and normalizes whitespace.
    Example: 'â€œHelloâ€\xa0World  ' → 'Hello World'
    """
    
    if not isinstance(text, str) or not text.strip():
        return None
```

```python
    # Normalize Unicode characters (fixes encoding issues)
    text = unicodedata.normalize("NFKC", text)
```

**Explanation**:
- Common problem: `â€œ` instead of `"`
- `normalize("NFKC", text)`: Converts to standard Unicode form
  - "NFKC" = Normalization Form KC (Compatibility Composition)
- Fixes:
  - `â€œ` → `"`
  - `â€™` → `'`
  - `â€"` → `—`
  - Non-breaking spaces → regular spaces

**Why this happens**: Website uses special Unicode, Python reads as different encoding.

```python
    # Remove non-printable characters
    text = "".join(ch for ch in text if ch.isprintable())
```

**Explanation**:
- `ch.isprintable()`: Returns True if character can be displayed
- Filters out: null bytes (`\x00`), control characters, etc.
- `"".join(...)`: Combines characters back into string
- Example: `"Hello\x00World"` → `"HelloWorld"`

```python
    # Normalize whitespace (replace multiple spaces with single space)
    text = re.sub(r"\s+", " ", text).strip()
```

**Explanation - Regex Breakdown**:
- `re.sub(pattern, replacement, string)`: Substitute using regex
- `r"\s+"`: Raw string (`r`), regex pattern
  - `\s`: Any whitespace character (space, tab, newline)
  - `+`: One or more occurrences
  - Matches: `"  "`, `"\n\n"`, `" \t "`, etc.
- `" "`: Replace with single space
- `.strip()`: Remove leading/trailing whitespace

**Example transformations**:
```python
"Hello    World" → "Hello World"
"Hello\n\nWorld" → "Hello World"
"  Hello  World  " → "Hello World"
```

**Apply to multiple columns**:
```python
df['education'] = df['education'].apply(clean_text)
df['address'] = df['address'].apply(clean_text)
df['specializations'] = df['specializations'].apply(clean_text)
df['biography'] = df['biography'].apply(clean_text)
df['research'] = df['research'].apply(clean_text)
```

#### Function 4: Clean and Categorize Phone Numbers

```python
def clean_and_categorize_phone(phone):
    """
    Categorizes phone numbers as mobile or landline.
    Example: '079-68261634, 9882114669' → 
             {'mobile': ['9882114669'], 'landline': ['07968261634']}
    """
    
    if not isinstance(phone, str) or not phone.strip():
        return None
```

```python
    # Remove hyphens and spaces
    phone_cleaned = phone.replace("-", "").replace(" ", "")
```

**Explanation**:
- Standardize format: `"079-6826-1634"` → `"07968261634"`
- Removes separators for consistent processing

```python
    # Initialize result dictionary
    result = {"mobile": [], "landline": []}
```

**Explanation**:
- Dictionary with two lists
- Will categorize numbers into these buckets

```python
    # Extract all digit sequences using regex
    for num in re.findall(r"\d+", phone_cleaned):
```

**Explanation**:
- `re.findall(r"\d+", text)`: Finds all sequences of digits
  - `\d`: Any digit (0-9)
  - `+`: One or more
- Example: `"Call 079-68261634 or 9882114669"` → `["079", "68261634", "9882114669"]`
- But we already cleaned, so: `"07968261634,9882114669"` → `["07968261634", "9882114669"]`

```python
        # Check if number is mobile (10 digits starting with 6-9)
        if len(num) == 10 and num[0] in "6789":
            result["mobile"].append(num)
```

**Explanation**:
- `len(num) == 10`: Indian mobile numbers are 10 digits
- `num[0]`: First character (first digit)
- `in "6789"`: Indian mobiles start with 6, 7, 8, or 9
- Example: `"9882114669"` → 10 digits, starts with 9 → mobile ✓

```python
        # Check if number is landline (starts with 0, 10-12 digits)
        elif num.startswith("0") and 10 <= len(num) <= 12:
            result["landline"].append(num)
```

**Explanation**:
- `num.startswith("0")`: Landlines start with 0 (STD code)
- `10 <= len(num) <= 12`: Landline length varies by region
  - Example: `"07968261634"` (11 digits)
- Both conditions must be True

```python
    # Remove empty categories
    result = {k: v for k, v in result.items() if v}
```

**Explanation - Dictionary Comprehension**:
- `result.items()`: Returns pairs like `("mobile", ["9882114669"])`
- `for k, v in ...`: Loop through key-value pairs
- `if v`: Only include if value (list) is not empty
- Example:
  ```python
  {"mobile": ["9882114669"], "landline": []}
  → {"mobile": ["9882114669"]}  # landline removed because empty
  ```

```python
    # Return dictionary or None if no valid numbers
    return result if result else None
```

**Example transformations**:
```python
Input: "079-68261634, 9882114669"
Output: {"mobile": ["9882114669"], "landline": ["07968261634"]}

Input: "9876543210"
Output: {"mobile": ["9876543210"]}

Input: "invalid"
Output: None
```

**Apply to column**:
```python
df['phone'] = df['phone'].apply(clean_and_categorize_phone)
```

#### Function 5: Clean Lists (Teaching, Publications)

```python
def clean_list(lst):
    """
    Cleans each item in a list and removes empty entries.
    Example: ['  Course 1  ', '', 'Course 2'] → ['Course 1', 'Course 2']
    """
    
    if not isinstance(lst, list):
        return None
```

```python
    cleaned = [
        clean_text(item)
        for item in lst
        if isinstance(item, str) and clean_text(item)
    ]
```

**Explanation - Breaking Down the List Comprehension**:

1. `for item in lst`: Loop through each item in list

2. `if isinstance(item, str)`: Only process strings
   - Filters out: `None`, numbers, etc.

3. `clean_text(item)`: Apply text cleaning function

4. `and clean_text(item)`: Only include if result is not None/empty

5. `[... for ...]`: Create new list with cleaned items

**Equivalent long form**:
```python
cleaned = []
for item in lst:
    if isinstance(item, str):
        cleaned_item = clean_text(item)
        if cleaned_item:  # Not None or empty
            cleaned.append(cleaned_item)
```

**Example**:
```python
Input: ['  Data Structures  ', '', '   Algorithms', None]
Step 1: Loop through items
Step 2: Filter strings → ['  Data Structures  ', '', '   Algorithms']
Step 3: Clean each → ['Data Structures', '', 'Algorithms']
Step 4: Filter non-empty → ['Data Structures', 'Algorithms']
Output: ['Data Structures', 'Algorithms']
```

```python
    return cleaned if cleaned else None
```

**Apply to column**:
```python
df['teaching'] = df['teaching'].apply(clean_list)
```

#### Function 6: Clean Publications (Advanced)

```python
def clean_publications(pub_list):
    """
    Merges fragmented publication entries into complete citations.
    Example: ['Author A,', 'Title of Paper,', 'Journal 2023']
             → ['Author A, Title of Paper, Journal 2023']
    """
    
    if not isinstance(pub_list, list):
        return None
    
    publications = []  # Final merged publications
    buffer = ""        # Temporary storage for fragments
```

**Why this is needed**:
- Web scraping might split one publication across multiple list items
- Example HTML:
  ```html
  <li>Author A,</li>
  <li>Title of Paper,</li>
  <li>Journal 2023</li>
  ```
- We want: `["Author A, Title of Paper, Journal 2023"]`
- Not: `["Author A,", "Title of Paper,", "Journal 2023"]`

```python
    for item in pub_list:
        if not isinstance(item, str):
            continue  # Skip non-string items
        
        item = clean_text(item)
        if not item:
            continue  # Skip empty items after cleaning
```

**Explanation**:
- `continue`: Skip to next iteration of loop
- Filters out invalid/empty items before processing

```python
        # Add current item to buffer
        buffer += " " + item
```

**Explanation**:
- Accumulates fragments
- Example:
  ```python
  buffer = ""
  buffer += " " + "Author A,"  # buffer = " Author A,"
  buffer += " " + "Title,"     # buffer = " Author A, Title,"
  ```

```python
        # Check if we have a complete publication
        # Publications typically contain year (1900-2099) or DOI
        if re.search(r"\b(19|20)\d{2}\b", buffer) or "doi" in buffer.lower():
```

**Explanation - Regex Pattern**:
- `\b`: Word boundary (ensures we match whole number, not part of another number)
- `(19|20)`: Matches 19 OR 20
- `\d{2}`: Exactly 2 digits
- `\b`: Word boundary
- Combined: Matches years 1900-2099
  - Matches: `"2023"`, `"1995"`
  - Doesn't match: `"23"` (too short), `"20234"` (too long)

```python
or "doi" in buffer.lower():
```
- Publications often have DOI (Digital Object Identifier)
- `.lower()`: Case-insensitive check
  - Matches: `"DOI"`, `"doi"`, `"Doi"`

**Why this works**:
- Complete publications usually include year and/or DOI
- Fragments (like just author name) don't
- When we find year/DOI, we know we have complete publication

```python
            publications.append(buffer.strip())  # Add to final list
            buffer = ""                           # Reset for next publication
```

```python
    # If buffer still has content at end, add it
    if buffer.strip():
        publications.append(buffer.strip())
```

**Explanation**:
- Last publication might not have year/DOI
- Don't want to lose it
- Example: `"Upcoming paper under review"` → added at end

```python
    return publications if publications else None
```

**Complete example**:
```python
Input: [
    "Smith, J.,",
    "Machine Learning Advances,",
    "Nature 2023",
    "Doe, A.,",
    "AI Research"
]

Processing:
buffer = " Smith, J.,"
buffer = " Smith, J., Machine Learning Advances,"
buffer = " Smith, J., Machine Learning Advances, Nature 2023"  # Found "2023"!
→ publications = ["Smith, J., Machine Learning Advances, Nature 2023"]
→ buffer = ""

buffer = " Doe, A.,"
buffer = " Doe, A., AI Research"  # No year, but end of list
→ publications = ["Smith, J., Machine Learning Advances, Nature 2023", 
                   "Doe, A., AI Research"]

Output: ["Smith, J., Machine Learning Advances, Nature 2023",
         "Doe, A., AI Research"]
```

**Apply to column**:
```python
df["publications"] = df["publications"].apply(clean_publications)
```

#### Function 7: Clean Website Links

```python
def clean_links(links):
    """
    Filters valid URLs and removes invalid entries.
    """
    
    if not isinstance(links, list):
        return None
    
    # Keep only strings that start with 'http'
    links = [l.strip() for l in links if isinstance(l, str) and l.startswith("http")]
    
    return links if links else None
```

**Explanation**:
- `l.startswith("http")`: Valid URLs start with `http://` or `https://`
- Filters out: relative paths (`/faculty/john`), invalid entries
- `.strip()`: Remove whitespace around URLs

**Apply**:
```python
df["website_links"] = df["website_links"].apply(clean_links)
```

#### Function 8: Categorize Website Links

```python
def categorize_links(links):
    """
    Organizes links by type (Google Scholar, LinkedIn, personal website, etc.)
    Example: ['https://scholar.google.com/...', 'https://linkedin.com/...']
             → {'google_scholar': [...], 'linkedin': [...]}
    """
    
    if not isinstance(links, list) or not links:
        return None
    
    # Initialize categories
    categorized = {
        "personal_website": [],
        "google_scholar": [],
        "linkedin": [],
        "youtube": [],
        "other": []
    }
```

```python
    for link in links:
        # Check domain and categorize
        if "scholar.google" in link:
            categorized["google_scholar"].append(link)
```

**Explanation**:
- `"scholar.google" in link`: Substring check
- Matches: `"https://scholar.google.com/citations?user=ABC"`
- Using `in` operator is simpler than regex for this case

```python
        elif "linkedin.com" in link:
            categorized["linkedin"].append(link)
        
        elif "youtube.com" in link or "youtu.be" in link:
            categorized["youtube"].append(link)
```

**Explanation**:
- `or`: Handles both YouTube domains
  - Full: `youtube.com`
  - Short: `youtu.be`

```python
        elif "sites.google" in link or "github.io" in link:
            categorized["personal_website"].append(link)
```

**Explanation**:
- Google Sites and GitHub Pages often used for personal academic sites

```python
        else:
            categorized["other"].append(link)
```

**Explanation**:
- Catchall for unrecognized links

```python
    # Remove empty categories
    categorized = {k: v for k, v in categorized.items() if v}
    
    return categorized if categorized else None
```

**Example**:
```python
Input: [
    "https://scholar.google.com/citations?user=ABC",
    "https://linkedin.com/in/johndoe",
    "https://example.com/research"
]

Output: {
    "google_scholar": ["https://scholar.google.com/citations?user=ABC"],
    "linkedin": ["https://linkedin.com/in/johndoe"],
    "other": ["https://example.com/research"]
}
```

**Apply**:
```python
df["website_links"] = df["website_links"].apply(categorize_links)
```

#### Normalize Empty Values to None

```python
# Convert empty strings and NaN to None
df = df.applymap(
    lambda x: None if isinstance(x, str) and not x.strip() else x
)
df = df.where(pd.notnull(df), None)
```

**Explanation**:
- `.applymap()`: Apply function to EVERY cell in DataFrame
- `lambda x:`: Anonymous function
- `isinstance(x, str) and not x.strip()`: Empty strings
- `pd.notnull(df)`: Checks each cell for NaN
- `.where(condition, value)`: If condition False, replace with value

**Why do this?**
- Database consistency
- `None` in Python = `NULL` in SQL
- Empty strings `""` ≠ NULL

#### Save Cleaned Data to CSV

```python
df.to_csv(
    "faculty_cleaned.csv",
    index=False
)
print("Cleaning completed and saved to faculty_cleaned.csv")
```

**Explanation**:
- `.to_csv()`: Writes DataFrame to CSV file
- `index=False`: Don't write row numbers as first column
- Without `index=False`, CSV would have:
  ```
  ,name,email
  0,John Doe,john@...
  1,Jane Smith,jane@...
  ```
- With `index=False`:
  ```
  name,email
  John Doe,john@...
  Jane Smith,jane@...
  ```

---

**File**: `data_clean.ipynb`

**Challenge**: Raw data contains:
- Encoding issues (â€œ instead of ")
- Inconsistent email formats (`yash[at]dau[dot]ac[dot]in`)
- Mixed phone number formats
- Fragmented publication entries

**Solution Examples**:

```python
# Email cleaning
def clean_email(email):
    email = email.replace("[at]", "@").replace("[dot]", ".")
    return email.split(",")  # Handle multiple emails

# Phone categorization
def clean_phone(phone):
    result = {"mobile": [], "landline": []}
    for num in phone.split(","):
        if len(num) == 10 and num[0] in "6789":
            result["mobile"].append(num)
        # ... landline logic
    return result
```

**Key learning**: Always handle missing values (`None`) and unexpected formats.

### Stage 3: Database Storage

**File**: Database creation in `data_clean.ipynb`

**Challenge**: Lists and dictionaries cannot be stored directly in SQLite.

**Solution**: Convert complex data to JSON strings before insertion.

```python
# Before inserting
df['phone'] = df['phone'].apply(json.dumps)  # {"mobile": ["9876543210"]} → string

# When reading from API
data = json.loads(phone_string)  # string → {"mobile": ["9876543210"]}
```

**Schema Design**:

```sql
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,              -- Stored as JSON array
    phone TEXT,              -- Stored as JSON object
    education TEXT,
    specializations TEXT,
    biography TEXT,
    research TEXT,
    teaching TEXT,           -- Stored as JSON array
    publications TEXT,       -- Stored as JSON array
    website_links TEXT,      -- Stored as JSON object
    faculty_type TEXT,
    address TEXT
);
```

**Why TEXT for everything?**
- SQLite doesn't have native list/dictionary types
- JSON strings preserve structure
- Easy to parse in Python
- Flexible for schema changes

### Stage 4: API Development (Serving)

**File**: `app/main.py`

**Challenge**: Data scientists need easy access to data without writing SQL queries.

**Solution**: FastAPI provides REST endpoints with automatic documentation.

```python
@app.get("/faculty/{faculty_id}")
def get_faculty(faculty_id: int):
    # Fetch from database
    # Parse JSON fields
    # Return structured response
```

**Key learning**: FastAPI automatically validates inputs and generates interactive documentation at `/docs`.

---

## Database Schema

### Faculty Table
| Column            | Type        | Description                             | Example                          |
| ----------------- | ----------- | --------------------------------------- | -------------------------------- |
| `id`              | INTEGER     | Auto-incremented primary key            | `1`, `2`, `3`                    |
| `faculty_type`    | TEXT        | Category of faculty                     | `"faculty"`, `"adjunct-faculty"` |
| `name`            | TEXT        | Full name in title case                 | `"Yash Vasavada"`                |
| `email`           | TEXT (JSON) | List of email addresses                 | `["yash@dau.ac.in"]`             |
| `phone`           | TEXT (JSON) | Categorized mobile and landline numbers | `{"mobile": ["9876543210"]}`     |
| `education`       | TEXT        | Academic degrees and institutions       | `"PhD (EE), Virginia Tech"`      |
| `address`         | TEXT        | Office location                         | `"#1224, FB-1, DA-IICT"`       |
| `specializations` | TEXT        | Research focus areas                    | `"Machine Learning, NLP"`        |
| `biography`       | TEXT        | Professional background summary         | `"Dr. X is a professor..."`      |
| `teaching`        | TEXT (JSON) | Courses taught                          | `["Data Structures", "AI"]`      |
| `research`        | TEXT        | Research interests                      | `"Computer Vision, Robotics"`    |
| `publications`    | TEXT (JSON) | List of research publications           | `["Paper 1...", "Paper 2..."]`   |
| `website_links`   | TEXT (JSON) | Categorized external links              | `{"google_scholar": ["url"]}`    |


**Total Records**: 111 faculty members

---

## API Documentation

### Base URL

```
http://127.0.0.1:8000
```

### Available Endpoints

#### 1. Get All Faculty

```http
GET /faculty
```

**Response**: Array of all 111 faculty members

**Example**:
```bash
curl http://127.0.0.1:8000/faculty
```

#### 2. Get Faculty by ID

```http
GET /faculty/{faculty_id}
```

**Parameters**:
- `faculty_id` (integer): Faculty ID (1-111)

**Example**:
```bash
curl http://127.0.0.1:8000/faculty/1
```

**Response**:
```json
{
  "id": 1,
  "name": "Yash Vasavada",
  "email": ["yash_vasavada@dau.ac.in"],
  "phone": {
    "landline": ["07968261634"]
  },
  "specializations": "Communication, Signal Processing",
  ...
}
```

#### 3. Filter by Faculty Type

```http
GET /faculty/type/{faculty_type}
```

**Parameters**:
- `faculty_type` (string): "faculty", "adjunct", "international", etc.

**Example**:
```bash
curl http://127.0.0.1:8000/faculty/type/faculty
```

#### 4. Search by Name

```http
GET /faculty/name/{faculty_name}
```

**Parameters**:
- `faculty_name` (string): Partial or full name (case-insensitive)

**Example**:
```bash
curl http://127.0.0.1:8000/faculty/name/yash
```

**Returns**: All faculty with "yash" in their name

### Interactive API Documentation

FastAPI provides automatic documentation:

1. Start the server: `uvicorn app.main:app --reload`
2. Visit: `http://127.0.0.1:8000/docs`
3. Try endpoints directly in browser (no Postman needed!)

---

## Data Dictionary

### Field Descriptions

**name**: Faculty member's full name in title case format. Cleaned from raw HTML to ensure consistency.

**email**: List of email addresses. Originally formatted as `user[at]domain[dot]com`, converted to standard `user@domain.com`. May contain multiple emails separated by commas.

**phone**: Dictionary categorizing numbers as:
- `mobile`: 10-digit numbers starting with 6-9
- `landline`: Numbers starting with 0 and 10-12 digits long

**education**: Academic qualifications including degree and institution. Example: "PhD (Electrical Engineering), IIT Bombay"

**specializations**: Research focus areas. Example: "Machine Learning, Computer Vision, Natural Language Processing"

**biography**: Professional background and career summary. May be long-form text (200-500 words).

**teaching**: List of courses taught. Example: `["Data Structures", "Machine Learning", "Algorithms"]`

**publications**: List of research papers. Fragments merged into complete entries during cleaning.

**website_links**: Dictionary categorizing links by type:
- `google_scholar`: Google Scholar profiles
- `linkedin`: LinkedIn profiles
- `personal_website`: Personal/academic websites
- `youtube`: YouTube channels
- `other`: Uncategorized links

### Data Quality Metrics

- **Total Records**: 111 faculty members
- **Missing Values**: Handled as `None` (NULL in database)
- **Encoding**: UTF-8 (special characters normalized)
- **Duplicates**: None (verified during cleaning)

---

## Troubleshooting

### Common Issues

#### 1. Scrapy Not Found

**Error**: `scrapy: command not found`

**Solution**:
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall scrapy
pip install scrapy
```

#### 2. Database Locked Error

**Error**: `sqlite3.OperationalError: database is locked`

**Solution**: Close all connections to `faculty.db`
```bash
# Kill any running Python processes
# Restart the API
uvicorn app.main:app --reload
```

#### 3. Import Errors in Jupyter

**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**: Install Jupyter in the same virtual environment
```bash
pip install jupyter pandas
jupyter notebook
```

#### 4. API Not Starting

**Error**: `Address already in use`

**Solution**: Port 8000 is occupied
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

#### 5. Empty Database

**Issue**: API returns empty arrays

**Solution**: Run the cleaning notebook again
```bash
jupyter notebook data_clean.ipynb
# Run all cells to regenerate faculty.db
```

---

## Future Enhancements

### Project 2: Semantic Search (Next Phase)

**Objective**: Build a natural language search engine for faculty expertise.

**User Query**: "Who works on sustainable energy and carbon capture?"

**System Response**: Returns faculty members working on related topics (renewable energy, environmental engineering) even if exact keywords don't match.

**Technical Approach**:

1. **Text Embeddings**: Convert biography and research text into vector representations
2. **Vector Database**: Store embeddings for fast similarity search
3. **Semantic Search**: Query using natural language, not exact keywords

**Tools to Learn**:
- Sentence Transformers (text → vectors)
- FAISS or ChromaDB (vector search)
- Streamlit (search interface)

### Potential Improvements

**Data Quality**:
- Add data validation (email format checks)
- Implement duplicate detection
- Handle missing data more gracefully

**API Features**:
- Add pagination for large result sets
- Implement full-text search across all fields
- Add filtering by multiple criteria

**Performance**:
- Cache frequently requested data
- Add request rate limiting
- Optimize database queries with indexes

**Deployment**:
- Dockerize the application
- Deploy to cloud (AWS, Heroku)
- Add authentication for API access

---

## Learning Outcomes

By completing this project, you now understand:

1. **Web Scraping**: How to extract data from websites using Scrapy
2. **Data Cleaning**: Handling messy real-world data with Pandas
3. **Database Design**: Structuring data for efficient storage and retrieval
4. **API Development**: Building RESTful services with FastAPI
5. **Data Engineering**: Complete pipeline from raw data to production API

**Next Steps**: Proceed to semantic search implementation (Project 2) to build an intelligent faculty discovery system.

---

## Contributing

This project was developed as a learning exercise. Contributions for improvements are welcome!

**Areas for contribution**:
- Additional data cleaning techniques
- More API endpoints
- Better error handling
- Test cases

---

## Acknowledgments

- DA-IICT for publicly available faculty data
- ChatGPT for assistance with debugging and learning FastAPI syntax
- Scrapy and FastAPI documentation teams

---

**Project Type**: Data Engineering Pipeline  
**Difficulty**: Beginner to Intermediate  
**Estimated Time**: 8-10 hours  
**Skills Gained**: Web scraping, data cleaning, SQL, REST APIs


---

**Project Type**: Data Engineering Pipeline  
**Difficulty**: Beginner to Intermediate  
**Estimated Time**: 8-10 hours  
**Skills Gained**: Web scraping, data cleaning, SQL, REST APIs


---

Here you go — **clean, minimal, and GitHub-ready**.
You can copy-paste this directly into your `README.md`.

---

## Project Authors

This project was collaboratively developed as part of an academic data engineering assignment.

### Team Members

**Manya Choradiya**

* College ID: `202518021`
* GitHub: [https://github.com/Manya123-web](https://github.com/)<Manya123-web>
* LinkedIn: [https://www.linkedin.com/in/manya-choradiya-383651361](https://www.linkedin.com/in/)<manya-choradiya-383651361>

**Ambuj Tripathi**

* College ID: `202518021`
* GitHub: [https://github.com/Shaneat8](https://github.com/)<Shaneat8>
* LinkedIn: [https://www.linkedin.com/in/ambujtripathi41](https://www.linkedin.com/in/)<ambujtripathi41>

