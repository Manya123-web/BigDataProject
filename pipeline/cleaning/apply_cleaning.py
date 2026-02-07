import sqlite3
import json
import re
import unicodedata
import os

# Paths relative to project root
DB_PATH = "pipeline/outputs/faculty.db"

def clean_text(text):
    if not isinstance(text, str) or not text.strip():
        return None
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ch.isprintable())
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_email(email):
    if not email: return None
    if isinstance(email, list):
        email = ",".join(email)
    email = email.replace("[at]", "@").replace("[dot]", ".")
    email = email.replace(" ", "")
    emails = [e for e in email.split(",") if "@" in e]
    return json.dumps(emails) if emails else None

def clean_and_categorize_phone(phone):
    if not phone: return None
    if isinstance(phone, dict):
        return json.dumps(phone)
    phone_cleaned = str(phone).replace("-", "").replace(" ", "")
    result = {"mobile": [], "landline": []}
    for num in re.findall(r"\d+", phone_cleaned):
        if len(num) == 10 and num[0] in "6789":
            result["mobile"].append(num)
        elif num.startswith("0") and 10 <= len(num) <= 12:
            result["landline"].append(num)
    result = {k: v for k, v in result.items() if v}
    return json.dumps(result) if result else None

def clean_list(lst):
    if not lst: return None
    try:
        if isinstance(lst, str):
            lst = json.loads(lst)
        if not isinstance(lst, list):
            return None
        cleaned = [clean_text(item) for item in lst if isinstance(item, str) and clean_text(item)]
        return json.dumps(cleaned) if cleaned else None
    except:
        return None

def clean_publications(pub_list):
    if not pub_list: return None
    try:
        if isinstance(pub_list, str):
            pub_list = json.loads(pub_list)
        if not isinstance(pub_list, list):
            return None
        publications = []
        buffer = ""
        for item in pub_list:
            item = clean_text(item)
            if not item: continue
            buffer += " " + item
            if re.search(r"\b(19|20)\d{2}\b", buffer) or "doi" in buffer.lower():
                publications.append(buffer.strip())
                buffer = ""
        if buffer.strip():
            publications.append(buffer.strip())
        return json.dumps(publications) if publications else None
    except:
        return None

def apply_cleaning():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    
    print(f"Cleaning {len(rows)} faculty records...")

    for row in rows:
        fid = row['id']
        updates = {}
        
        updates['name'] = (row['name'].title() if row['name'] else None)
        updates['email'] = clean_email(row['email'])
        updates['phone'] = clean_and_categorize_phone(row['phone'])
        updates['education'] = clean_text(row['education'])
        updates['address'] = clean_text(row['address'])
        updates['specializations'] = clean_text(row['specializations'])
        updates['biography'] = clean_text(row['biography'])
        updates['research'] = clean_text(row['research'])
        updates['teaching'] = clean_list(row['teaching'])
        updates['publications'] = clean_publications(row['publications'])
        
        # Build UPDATE query
        cols = []
        vals = []
        for k, v in updates.items():
            cols.append(f"{k} = ?")
            vals.append(v)
        vals.append(fid)
        
        cursor.execute(f"UPDATE faculty SET {', '.join(cols)} WHERE id = ?", vals)

    conn.commit()
    conn.close()
    print("Database cleaning completed!")

if __name__ == "__main__":
    apply_cleaning()
