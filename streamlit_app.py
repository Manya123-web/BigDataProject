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

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stMainContainer {padding: 0 !important;}
        .stApp {background: transparent;}
        [data-testid="stHeader"] {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        iframe {border: none !important; width: 100% !important;}
    </style>
""", unsafe_allow_html=True)

db = SessionLocal()

def parse_faculty_json(f):
    """Parse JSON fields in faculty data"""
    json_fields = ["phone", "email", "teaching", "publications", "website_links"]
    for field in json_fields:
        if f.get(field):
            try:
                if isinstance(f[field], str):
                    f[field] = json.loads(f[field])
            except Exception as e:
                print(f"Error parsing {field}: {e}")
                pass
    return f

query = st.query_params.get("q", "")
results = []

if query:
    try:
        results = search_faculty(query, k=50)
        for r in results:
            parse_faculty_json(r)
    except Exception as e:
        st.error(f"Error performing search: {e}")
else:
    try:
        res = db.execute(text("SELECT * FROM faculty LIMIT 200"))
        results = [dict(row) for row in res.mappings().all()]
        for r in results:
            r["similarity_score"] = 1.0
            parse_faculty_json(r)
    except Exception as e:
        st.error(f"Error loading faculty: {e}")

html_path = Path("app/static/index.html")
if not html_path.exists():
    st.error(f"HTML file not found at {html_path}")
    st.stop()

html_template = html_path.read_text(encoding="utf-8")

data_injection = f"""
<script>
    window.INJECTED_RESULTS = {json.dumps(results, ensure_ascii=False)};
    window.CURRENT_QUERY = {json.dumps(query)};
</script>
"""

html_content = html_template.replace("</body>", f"{data_injection}</body>")

st.components.v1.html(
    html_content,
    height=3000,  
    scrolling=True
)

db.close()