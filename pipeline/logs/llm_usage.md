# LLM Usage Log

This document tracks all interactions with ChatGPT (GPT-4) during the Faculty Finder project development.

---

## Session Overview

**LLM Tool Used**: ChatGPT (GPT-5.2)  
**Total Sessions**: 5   
**Purpose**: Learning assistance, debugging, and syntax guidance

**Key Areas Where LLM Was Used**:
1. Selecting Scrapy CSS selectors
2. Data cleaning strategies with Industry standards
3. FastAPI setup and syntax
4. Documentation formatting

**Key Areas Completed Independently**:
1. Web Scraping 
2. SQLite database connection and schema design
3. Data transformation logic implementation
4. Overall project architecture decisions
5. Testing and validation

---

## Session 1: Web Scraping Setup

### Problem Context

I had worked with scrapy and to increase the speed of project used LLM to find suitable selectors by giving it the list of items i will store and html structure of the site to be scraped, Further assistance was required for:
- Writing correct CSS selectors for nested HTML
- Handling pagination across multiple faculty categories (providing the instructions of what to fetch )
- Missing and Incorrect data fields (specializations, publications not extracting)
- One Faculty had different structure from others so changes accordingly

### Query to ChatGPT

**Prompt**:
```
I am scarping data from DAIICT website about faculty information , aldready setup with scapry and these are the list of items to be fetched

import scrapy
class FacultyFinderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    education = scrapy.Field()
    biography = scrapy.Field()
    specializations = scrapy.Field()
    teaching = scrapy.Field()
    publications = scrapy.Field()
    research = scrapy.Field()
    website_links = scrapy.Field()
    faculty_type = scrapy.Field()
    
    pass
```
:

[pasted initial spider code]

The HTML structure for the site looks like:

[pasted HTML structure ]


```

### ChatGPT Response Summary

**Key Points**:
1. Explained CSS selector hierarchy and how to target nested elements
2. Suggested using `::text` vs `.text()` for different scraping scenarios
3. Recommended using `get()` vs `getall()` based on single vs multiple values
4. Provided corrected selector syntax

**Suggested Solution**:
```python
# Instead of:
specializations = response.css('div.field--name-field-specializations::text').get()

# Use:
specializations = response.css(
    'div.field--name-field-specializations .field__item *::text'
).getall()
specializations = ' '.join(specializations).strip()
```

**Explanation**: The `*::text` selector captures all text nodes within child elements, handling cases where content is spread across multiple tags.

### What I Learned

- CSS selector specificity matters
- `getall()` returns a list, `get()` returns first match
- Using `*::text` captures nested text content
- Need to handle empty/missing fields with conditional logic

### What I Implemented Myself

After understanding the selector pattern, I:
1. Applied similar logic to extract publications and biography
2. Added error handling for missing fields
3. Implemented fallback selectors for inconsistent HTML structure
4. Created the iteration logic to visit all faculty profile pages
5. Verified the scraped data

---

## Session 2: Data Cleaning Strategies

### Problem Context

After scraping, I had messy data:
- Email format: `yash[at]dau[dot]ac[dot]in`
- Phone numbers mixed together: `079-68261634, 9882114669`
- Publications split into fragments
- Encoding issues with special characters (â€œ instead of ")

### Query to ChatGPT

**Prompt**:
```
I have scraped faculty data but emails are formatted as "name[at]domain[dot]com" 
and phone numbers are mixed (both mobile and landline in one string). 
How do I clean this data using Pandas and in a industry accepted manner? 

Also, some text has encoding issues like â€œ instead of quotes. 
What's the best approach to fix this?
```

### ChatGPT Response Summary

**Key Points**:
1. Use string `.replace()` for simple pattern substitution
2. Regular expressions for pattern matching (phone number formats)
3. Python's `unicodedata.normalize()` for fixing encoding
4. Categorizing data using conditional logic

**Suggested Approach for Emails**:
```python
def clean_email(email):
    if not isinstance(email, str) or not email.strip():
        return None
    
    email = email.replace("[at]", "@").replace("[dot]", ".")
    emails = [e.strip() for e in email.split(",")]
    return emails
```

**Suggested Approach for Encoding**:
```python
import unicodedata

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### What I Learned

- `unicodedata.normalize()` fixes mojibake (garbled characters)
- Regular expressions pattern: `\d+` matches digits
- Categorization logic using dictionary structures
- Importance of handling None/empty values

### What I Implemented Myself

I independently created:
1. Phone categorization logic (mobile vs landline based on length and starting digit)
2. Publication merging algorithm to join fragmented entries
3. Website link categorization (Google Scholar, LinkedIn, personal sites)
4. Complete data validation to ensure no corrupt records

**My Phone Cleaning Function**:
```python
def clean_and_categorize_phone(phone):
    result = {"mobile": [], "landline": []}
    
    for num in re.findall(r'\d+', phone):
        if len(num) == 10 and num[0] in '6789':
            result["mobile"].append(num)
        elif num.startswith('0') and 10 <= len(num) <= 12:
            result["landline"].append(num)
    
    return {k: v for k, v in result.items() if v} or None
```

---

## Session 3: SQLite Database Connection

### Problem Context

**This section was completed independently without LLM assistance.**

I designed the database schema based on my understanding of:
- Faculty data structure
- Need to store lists/dictionaries as JSON
- Primary key design
- NULL handling

### Implementation Details

**Schema Design** (My work):
```python
cursor.execute("""
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_type TEXT,
    name TEXT,
    email TEXT,           -- JSON array
    phone TEXT,           -- JSON object
    education TEXT,
    specializations TEXT,
    biography TEXT,
    research TEXT,
    teaching TEXT,        -- JSON array
    publications TEXT,    -- JSON array
    website_links TEXT,   -- JSON object
    address TEXT
)
""")
```

**Data Insertion Logic** (My work):
```python
# Convert lists/dicts to JSON before insertion
for col in ['phone', 'email', 'teaching', 'publications', 'website_links']:
    df[col] = df[col].apply(lambda x: json.dumps(x) if x else None)

# Use SQLAlchemy to insert
engine = create_engine("sqlite:///faculty.db")
df.to_sql("faculty", con=engine, if_exists="replace", index=False)
```

### Key Decisions Made Independently

1. **Why TEXT for everything**: SQLite doesn't support array/object types natively
2. **JSON serialization**: Preserves complex data structures
3. **Primary key**: Auto-increment for easy referencing
4. **NULL handling**: Used None in Python, translates to NULL in SQLite

---

## Session 4: FastAPI Setup and Syntax

### Problem Context

I wanted to create REST API endpoints but had never used FastAPI before. I needed the understanding of:
- Basic FastAPI project structure
- How to connect to SQLite database
- Defining response models with Pydantic
- Parsing JSON fields when retrieving data

### Query to ChatGPT

**Prompt**:
```
I have a SQLite database with faculty data where some fields are stored as JSON strings. 
I want to create a FastAPI application with endpoints to:
1. Get all faculty
2. Get faculty by ID
3. Filter by faculty type

I'm new to FastAPI. Can you show me the basic structure for:
- Connecting to SQLite using SQLAlchemy
- Defining Pydantic models for response validation
- Writing route handlers that parse JSON fields back to Python objects
```

### ChatGPT Response Summary

**Key Points**:
1. FastAPI uses decorators (`@app.get()`) to define routes
2. SQLAlchemy manages database connections
3. Pydantic models validate response structure
4. Need to parse JSON strings back to Python objects before returning

**FastAPI Basic Structure**:
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/faculty")
def get_all_faculty(db: Session = Depends(get_db)):
    # Query database
    # Return results
```

**Database Connection Pattern**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///faculty.db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Pydantic Model Example**:
```python
from pydantic import BaseModel
from typing import Optional, List, Dict

class FacultyOut(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[List[str]]
    phone: Optional[Dict[str, List[str]]]
```

### What I Learned

- `Depends(get_db)` provides dependency injection for database sessions
- Pydantic models auto-validate response data types
- `response_model` parameter ensures type-safe API responses
- Need to manually parse JSON strings from database

### What I Implemented Myself

After learning the syntax, I independently built:

1. **JSON Parsing Logic**:
```python
JSON_FIELDS = {"phone", "email", "teaching", "publications", "website_links"}

def parse_row(row: dict) -> dict:
    data = dict(row)
    for field in JSON_FIELDS:
        value = data.get(field)
        if value:
            try:
                data[field] = json.loads(value)
            except:
                data[field] = None
    return data
```

2. **Complete API Routes**:
- `/faculty` - Get all faculty
- `/faculty/{id}` - Get by ID
- `/faculty/type/{type}` - Filter by type
- `/faculty/name/{name}` - Search by name (my addition)

3. **Error Handling**:
```python
if not row:
    raise HTTPException(status_code=404, detail="Faculty not found")
```

4. **Redirect to Docs**:
```python
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
```

---

## Session 5: Documentation and README Formatting

### Problem Context

I wanted to create a comprehensive README that:
- Explains the project to beginners
- Documents the data pipeline clearly
- Includes setup instructions
- Provides API documentation

### Query to ChatGPT

**Prompt**:
```
I need to create a README.md for my faculty scraping project. 
It should be beginner-friendly for data scientists who want to understand:
1. What the project does
2. How to set it up
3. How the data pipeline works
4. API endpoints available

The project involves web scraping, data cleaning, SQLite storage, and FastAPI. 
Can you help structure a comprehensive README?
```

### ChatGPT Response Summary

**Key Points**:
1. Start with clear project overview and objectives
2. Include table of contents for long READMEs
3. Use code blocks for commands and examples
4. Add troubleshooting section for common errors
5. Include data dictionary for field descriptions

**Recommended Structure**:
```markdown
# Project Title
## Overview
## Technologies
## Setup
## How to Run
## Understanding the Pipeline
## API Documentation
## Troubleshooting
```

### What I Implemented Myself

I took the structural guidance and created:
1. Detailed explanations of each pipeline stage
2. Real-world examples for each cleaning function
3. Complete API documentation with curl examples
4. Database schema explanation
5. Future enhancements section

**My additions not suggested by ChatGPT**:
- Visual project structure diagram
- Data quality metrics
- Learning outcomes section
- Comparison of why TEXT is used for all SQLite fields

---

## Key Takeaways

### What ChatGPT Was Good For

1. **Learning Syntax**: Understanding FastAPI decorators, Pydantic syntax
2. **Pattern Recognition**: Seeing examples of regex, CSS selectors
3. **Best Practices**: Understanding proper error handling approaches
4. **Debugging Ideas**: Getting suggestions when stuck on specific errors

### What I Had to Figure Out Myself

1. **Business Logic**: How to categorize phone numbers, merge publications
2. **Architecture Decisions**: Database schema, API endpoint design
3. **Edge Cases**: Handling missing data, malformed inputs
4. **Integration**: Connecting all pipeline stages together
5. **Testing**: Verifying data quality, API functionality
