# LLM Usage Log

This document tracks all interactions with ChatGPT (GPT-4) during the Faculty Finder project development.

---

## Session Overview

**LLM Tool Used**: ChatGPT (GPT-4)  
**Total Sessions**: 4  
**Date Range**: [Your project dates]  
**Purpose**: Learning assistance, debugging, and syntax guidance

**Key Areas Where LLM Was Used**:
1. Web scraping logic and Scrapy CSS selectors
2. Data cleaning strategies
3. FastAPI setup and syntax
4. Documentation formatting

**Key Areas Completed Independently**:
1. SQLite database connection and schema design
2. Data transformation logic implementation
3. Overall project architecture decisions
4. Testing and validation

---

## Session 1: Web Scraping Setup

### Problem Context

I needed to scrape faculty data from DA-IICT website but was struggling with:
- Understanding Scrapy project structure
- Writing correct CSS selectors for nested HTML
- Handling pagination across multiple faculty categories
- Missing data fields (specializations, publications not extracting)

### Query to ChatGPT

**Prompt**:
```
I'm trying to scrape faculty information from a college website using Scrapy. 
The website has faculty profiles with name, email, education, and research interests. 
I've written basic code but it's not extracting specializations and publications. 
Here's my current spider code:

[pasted initial spider code]

The HTML structure for specializations looks like:
<div class="field--name-field-specializations">
  <div class="field__item">Machine Learning, AI</div>
</div>

How do I fix my selectors to extract this data?
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
How do I clean this data using Pandas? 

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

I wanted to create REST API endpoints but had never used FastAPI before. I needed to understand:
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

## Summary of LLM Usage vs Independent Work

### Areas Where ChatGPT Helped (Learning)

| Task | ChatGPT's Role | What I Learned |
|------|----------------|----------------|
| CSS Selectors | Explained syntax and hierarchy | How to target nested HTML elements |
| Data Cleaning | Suggested string manipulation patterns | unicodedata, regex patterns |
| FastAPI Syntax | Provided basic structure and decorators | Dependency injection, Pydantic models |
| Documentation | Recommended README structure | How to write beginner-friendly docs |

### Areas Completed Independently (Application)

| Task | Implementation | Complexity |
|------|---------------|------------|
| Database Schema Design | Created entire SQLite structure | Medium |
| Phone Categorization Logic | Built mobile/landline detection | Medium |
| Publication Merging Algorithm | Developed fragment joining logic | High |
| Website Link Categorization | Classified links by type | Low |
| All API Route Logic | Implemented 4 endpoints + error handling | Medium |
| JSON Parsing in API | Created parse_row() function | Medium |
| Complete Data Validation | Ensured data quality across pipeline | High |

### Percentage Breakdown

- **LLM-Assisted Learning**: ~30% (syntax, patterns, best practices)
- **Independent Implementation**: ~70% (logic, architecture, testing)

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

### Lessons Learned About Using LLMs

**Effective Prompting**:
- Provide specific context (code snippets, error messages)
- Ask for explanations, not just solutions
- Request examples to understand patterns

**Where LLMs Excel**:
- Syntax and boilerplate code
- Explaining concepts with examples
- Suggesting alternative approaches

**Where Human Judgment Is Crucial**:
- Understanding project requirements
- Making architectural decisions
- Validating data quality
- Optimizing for specific use cases

---

## Ethical Use Statement

All LLM assistance was used for:
- Learning new technologies (FastAPI, advanced Scrapy features)
- Understanding syntax and best practices
- Getting unstuck on specific problems

All core logic, architecture, and implementation decisions were made independently. This project represents genuine learning and skill development, with ChatGPT serving as a tutoring tool rather than a solution generator.

---

**Total Tokens Used**: Approximately 15,000 tokens across all sessions  
**Time Saved**: Estimated 4-5 hours of documentation reading  
**Skills Gained**: FastAPI, advanced Pandas, Pydantic, REST API design