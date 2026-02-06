import streamlit as st
from pathlib import Path
import json
from pipeline.recommender.search import search_faculty
from sqlalchemy import text
from app.db import SessionLocal

st.set_page_config(page_title="Faculty Recommender AI",layout="wide")

# Initialize database session
db = SessionLocal()

# helper for JSON parsing
def parse_faculty_json(f):
    json_fields = ["phone", "email", "teaching", "publications", "website_links"]
    for field in json_fields:
        if f.get(field):
            try:
                if isinstance(f[field], str):
                    f[field] = json.loads(f[field])
            except Exception:
                pass
    return f

# Native Streamlit search fallback
st.title("Academic Search")
query_input = st.text_input("Search Faculty", value=st.query_params.get("q", ""), key="st_query")

# Update query param and trigger reload if changed via native search
if query_input != st.query_params.get("q", ""):
    st.query_params["q"] = query_input
    st.rerun()

# Handle search query
query = st.query_params.get("q", "")
results = []

if query:
    results = search_faculty(query, k=50) # Increased search k
    for r in results:
        parse_faculty_json(r)
else:
    # Default to all faculty if no query
    try:
        res = db.execute(text("SELECT * FROM faculty LIMIT 200")) # Increased limit to 200
        results = [dict(row) for row in res.mappings().all()]
        for r in results:
            r["similarity_score"] = 1.0
            parse_faculty_json(r)
    except Exception as e:
        st.error(f"Error loading faculty: {e}")

# Read the HTML file
html_template = Path("app/static/index.html").read_text(encoding="utf-8")

# Inject data into the HTML
data_injection = f"""
<script>
    window.INJECTED_RESULTS = {json.dumps(results)};
    window.CURRENT_QUERY = {json.dumps(query)};
</script>
"""

# Insert before </body>
html_content = html_template.replace("</body>", f"{data_injection}</body>")

# Render the HTML component
# Use a dynamic height or stick to a large enough value
st.components.v1.html(
    html_content,
    height=1200,
    scrolling=True
)