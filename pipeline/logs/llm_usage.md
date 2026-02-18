# LLM Usage Log

This document records all interactions with ChatGPT (GPT-5.2) during the development of the **Faculty Finder Project**, including scraping, data processing, API development, recommender system integration, and UI deployment.

---

## Session Overview

**LLM Tool Used**: ChatGPT (GPT-5.2)
**Total Sessions**: 8
**Purpose**: Concept clarification, debugging assistance, architectural guidance, recommender system design support, and UI troubleshooting.

The LLM was primarily used as a learning assistant and debugging aid rather than a code-generation dependency.

---

# Session 1: Web Scraping Setup & CSS Selection

### Prompt:

```
How to write correct CSS selectors for nested HTML and handle inconsistent faculty data fields in Scrapy?
```

### Summary:

Guidance was provided on identifying stable CSS selectors within deeply nested HTML structures. The explanation covered differences between `.get()` and `.getall()`, handling optional fields, and writing fallback selectors to manage inconsistent faculty profile formats. Best practices for avoiding selector brittleness and improving scraping robustness were also discussed.

---

# Session 2: Data Cleaning & Normalization

### Prompt:

```
How to clean emails like "name[at]domain[dot]com", mixed phone numbers, and fix encoding issues in Pandas?
```

### Summary:

The LLM suggested using regular expressions to standardize phone number formats, string replacement techniques to normalize obfuscated email addresses, and `unicodedata.normalize()` for resolving encoding inconsistencies. It also recommended applying vectorized Pandas operations for performance and maintaining reproducibility in cleaning functions.

---

### Prompt:

```
How to handle missing values and inconsistent list-type fields before inserting into SQLite?
```

### Summary:

Guidance was provided on converting lists and dictionaries into JSON strings before database insertion, ensuring NULL handling through Python’s `None`, and maintaining schema consistency. It clarified why SQLite requires TEXT storage for complex structures and how to preserve data integrity during serialization.

---

# Session 3: FastAPI Development & API Validation

### Prompt:

```
How to build FastAPI endpoints for a SQLite database with JSON fields and validate responses using Pydantic?
```

### Summary:

The LLM provided architectural guidance on structuring FastAPI routes, connecting to SQLite via SQLAlchemy, and validating structured responses using Pydantic models. It explained how to parse JSON fields back into Python objects before returning API responses, ensuring type safety and clean API documentation through automatic schema generation.

---

### Prompt:

```
How to structure error handling and response models in FastAPI?
```

### Summary:

Recommendations included using HTTPException for proper status codes, defining consistent response schemas, and separating service logic from route definitions for cleaner maintainability. Emphasis was placed on clarity and scalability of API design.

---

# Session 4: Documentation & Project Structuring

### Prompt:

```
How to structure a beginner-friendly README for a faculty scraping project with scraping, cleaning, SQLite, and FastAPI?
```

### Summary:

Suggested organizing documentation into structured sections including project overview, architecture, setup instructions, pipeline flow, API documentation, database schema explanation, troubleshooting, and future improvements. Emphasis was placed on clarity, reproducibility, and professional presentation standards.

---

# Session 5: Recommender System Architecture

### Prompt:

```
Which recommender system is most suitable for faculty expertise search?
```

### Summary:

The LLM analyzed the problem context and recommended a **content-based recommender system**, as no user interaction history was available. It explained that faculty expertise search relies on textual similarity across research interests, publications, and teaching domains, making content-based filtering the most appropriate approach.

It also briefly compared:

* Collaborative filtering (not suitable without user data)
* Hybrid systems (requires larger scale and interaction logs)
* Content-based semantic matching (recommended solution)

---

### Prompt:

```
Should I use TF-IDF or Sentence Transformers for semantic similarity?
```

### Summary:

The LLM compared traditional TF-IDF vectorization with transformer-based embeddings. It explained that TF-IDF captures keyword frequency but lacks contextual understanding, whereas Sentence Transformers generate semantic embeddings that capture contextual similarity between research descriptions. Based on scalability and accuracy needs, transformer-based embeddings were recommended.

---

# Session 6: Sentence Transformer Integration & Pipeline Issues

### Prompt:

```
How to implement Sentence Transformers for semantic similarity search?
```

### Summary:

Provided guidance on installing and loading pre-trained models (e.g., `all-mpnet-base-v2`), encoding combined faculty text fields, generating embeddings, and computing cosine similarity scores. It also explained how to store embeddings and reuse them efficiently without recomputation.

---

### Prompt:

```
Why is my newly added transformer pipeline node not loading in main.py?
```

### Summary:

Suggested debugging module imports, ensuring proper node registration in the pipeline configuration, verifying file structure consistency, checking for missing `__init__.py`, and resolving circular import issues.

---

### Prompt:

```
After implementing Sentence Transformers, I started getting module/path errors. How can I resolve this?
```

### Summary:

Recommended verifying virtual environment activation, confirming library installation, resolving relative vs absolute import conflicts, ensuring consistent Python interpreter usage, and correcting project root path configuration.

---

# Session 7: Streamlit Integration & UI Development

### Prompt:

```
How to set up Streamlit for integrating the faculty recommender system?
```

### Summary:

Guided on setting up `streamlit_app.py`, running Streamlit correctly, creating search inputs, displaying ranked faculty results, and connecting Streamlit frontend with FastAPI backend endpoints.

---

### Prompt:

```
How to manage state in Streamlit for multiple pages?
```

### Summary:

Explained usage of `st.session_state`, sidebar navigation patterns, conditional rendering logic, and preventing unwanted state resets on refresh or page transitions.

---

### Prompt:

```
Streamlit navigation is not working properly. How can I fix page switching issues?
```

### Summary:

Recommended structured routing logic, consistent state variables, and avoiding reinitialization of variables during reruns.

---

# Session 8: OpenAlex API Integration Debugging

### Prompt:

```
OpenAlex data is being fetched but not displaying in Streamlit. What could be the issue?
```

### Summary:

Suggested debugging by printing raw API responses, validating JSON key structure, confirming loop iteration over returned data, handling empty lists safely, and ensuring compatibility between backend response format and Streamlit rendering logic.

---

### Prompt:

```
How to safely handle external API failures in Streamlit?
```

### Summary:

Advised implementing try-except blocks, displaying user-friendly error messages, validating response status codes, and handling timeouts gracefully.