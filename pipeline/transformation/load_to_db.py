import pandas as pd
import json
import sqlite3
from sqlalchemy import create_engine
from collections import defaultdict


df = pd.read_csv("pipeline/data/processed/faculty_cleaned.csv")

# %%
JSON_COLUMNS = [
    "phone",
    "email",
    "teaching",
    "publications",
    "website_links"
]

def to_json_safe(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return None if pd.isna(value) else value

for col in JSON_COLUMNS:
    df[col] = df[col].apply(to_json_safe)

# %%
column_types = defaultdict(set)

for col in df.columns:
    for val in df[col]:
        if val is not None:
            column_types[col].add(type(val).__name__)

column_types


# %%
DB_PATH = "pipeline/outputs/faculty.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
try :
    cursor.execute("DROP TABLE IF EXISTS faculty")

    cursor.execute("""
    CREATE TABLE faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_type TEXT,
        name TEXT,
        education TEXT,
        phone TEXT,
        address TEXT,
        email TEXT,
        specializations TEXT,
        biography TEXT,
        teaching TEXT,
        research TEXT,
        publications TEXT,
        website_links TEXT,
        image_url TEXT,
        openalex_id TEXT,
        citations INTEGER DEFAULT 0,
        works_count INTEGER DEFAULT 0,
        topics TEXT
    )""")

    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error creating database table: {e}")

# %%
df = df.reset_index(drop=True)
df.insert(0, "id", range(1, len(df) + 1))

df['faculty_type'].unique()

# %%
try:
    from sqlalchemy import create_engine

    engine = create_engine(f"sqlite:///{DB_PATH}")

    df.to_sql(
        "faculty",
        con=engine,
        if_exists="append",
        index=False
    )
    print("Data inserted into faculty.db successfully.")
except Exception as e:
    print(f"Error inserting data into database: {e}")


# %%
try:
    conn = sqlite3.connect(DB_PATH)

    result = pd.read_sql(
        "SELECT * FROM faculty LIMIT 3",
        conn
    )

    print(result)
    conn.close()
except Exception as e:
    print(f"Error querying database: {e}")
