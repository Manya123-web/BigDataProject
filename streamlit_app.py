import streamlit as st
from pathlib import Path
import json
from pipeline.recommender.search import search_faculty
from sqlalchemy import text
from app.db import SessionLocal

st.set_page_config(
    page_title="Faculty Recommender AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database session
db = SessionLocal()

# Handle search query from URL params
query = st.query_params.get("q", "")
results = []

if query:
    results = search_faculty(query, k=25)
else:
    # Default to all faculty if no query
    try:
        res = db.execute(text("SELECT * FROM faculty LIMIT 50"))
        results = [dict(row) for row in res.mappings().all()]
        # Add default similarity for initial view
        for r in results:
            r["similarity_score"] = 1.0
    except Exception as e:
        st.error(f"Error loading faculty: {e}")

# Read the HTML file
html_template = Path("app/static/index.html").read_text(encoding="utf-8")

# Inject data into the HTML
# We prepend the data as global variables before the closing body tag
data_injection = f"""
<script>
    window.INJECTED_RESULTS = {json.dumps(results)};
    window.CURRENT_QUERY = {json.dumps(query)};
</script>
"""

# Insert before </body>
html_content = html_template.replace("</body>", f"{data_injection}</body>")

# Render the HTML component
st.components.v1.html(
    html_content,
    height=1000,
    scrolling=True
)