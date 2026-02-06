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

# Custom CSS for Full Screen
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

# Initialize database session
db = SessionLocal()

# Helper for JSON parsing
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
    return f

# Handle search query from URL parameters
query = st.query_params.get("q", "")
results = []

try:
    if query:
        # Perform semantic search
        print(f"Searching for: {query}")
        results = search_faculty(query, k=50)
        print(f"Found {len(results)} results")
        for r in results:
            parse_faculty_json(r)
    else:
        # Default to all faculty if no query
        print("Loading all faculty...")
        res = db.execute(text("SELECT * FROM faculty LIMIT 200"))
        results = [dict(row) for row in res.mappings().all()]
        print(f"Loaded {len(results)} faculty members")
        for r in results:
            r["similarity_score"] = 1.0
            parse_faculty_json(r)
            
    print(f"Total results to inject: {len(results)}")
    
except Exception as e:
    st.error(f"Database Error: {e}")
    import traceback
    st.error(traceback.format_exc())
    results = []

# Read the HTML file
html_path = Path("app/static/index.html")
if not html_path.exists():
    st.error(f"HTML file not found at {html_path}")
    st.error(f"Current directory: {Path.cwd()}")
    st.error(f"Looking for: {html_path.absolute()}")
    st.stop()

try:
    html_template = html_path.read_text(encoding="utf-8")
    print("HTML template loaded successfully")
except Exception as e:
    st.error(f"Error reading HTML file: {e}")
    st.stop()

# Inject data into the HTML - ensure proper escaping
try:
    # Convert results to JSON string
    results_json = json.dumps(results, ensure_ascii=False, indent=None)
    query_json = json.dumps(query, ensure_ascii=False)
    
    print(f"JSON data prepared - Results: {len(results)}, Query: '{query}'")
    
    # Create the injection script with console logging
    data_injection = f"""<script>
(function() {{
    console.log('=== Faculty Recommender: Injecting Data ===');
    try {{
        window.INJECTED_RESULTS = {results_json};
        window.CURRENT_QUERY = {query_json};
        console.log('✓ INJECTED_RESULTS set:', window.INJECTED_RESULTS ? window.INJECTED_RESULTS.length + ' faculty members' : 'ERROR: undefined');
        console.log('✓ CURRENT_QUERY set:', window.CURRENT_QUERY);
        
        // Also log first faculty member for verification
        if (window.INJECTED_RESULTS && window.INJECTED_RESULTS.length > 0) {{
            console.log('✓ First faculty:', window.INJECTED_RESULTS[0].name);
        }}
    }} catch (e) {{
        console.error('✗ Error injecting data:', e);
    }}
}})();
</script>
"""

    # Insert before </head> for earlier execution
    if "</head>" in html_template:
        html_content = html_template.replace("</head>", f"{data_injection}</head>")
        print("Data injected into <head>")
    else:
        # Fallback to body if no head tag
        html_content = html_template.replace("</body>", f"{data_injection}</body>")
        print("Data injected into <body>")
    
except Exception as e:
    st.error(f"Error preparing HTML injection: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

# Show a status message
if results:
    st.success(f"✓ Loaded {len(results)} faculty members" + (f" for query: '{query}'" if query else ""))
else:
    st.warning("⚠ No faculty data loaded")

# Render the HTML component
try:
    st.components.v1.html(
        html_content,
        height=3000,
        scrolling=True
    )
except Exception as e:
    st.error(f"Error rendering component: {e}")
    import traceback
    st.error(traceback.format_exc())

# Close database session
try:
    db.close()
except:
    pass