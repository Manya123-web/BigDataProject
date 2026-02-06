# %%
import pandas as pd
import json
import re
import unicodedata

df=pd.read_json("../data/raw/faculty_output.json")
print(f"Data loaded: {len(df)} rows")

# %%
df.head(5)

# %%
def title_case_name(name):
    if not isinstance(name, str) or name.strip() == "":
        return None
    return name.title()

df['name'] = df['name'].apply(title_case_name)

# %%
def clean_email(email):
    if not isinstance(email, str) or not email.strip():
        return None

    email = email.replace("[at]", "@").replace("[dot]", ".")
    email = email.replace(" ", "")

    emails = [e for e in email.split(",") if "@" in e]

    return emails if emails else None

df['email'] = df['email'].apply(clean_email)

# %%

def clean_text(text):
    if not isinstance(text, str) or not text.strip():
        return None

    # Normalizing unicode (fixes most encoding issues)
    text = unicodedata.normalize("NFKC", text)

    # Remove non-printable characters
    text = "".join(ch for ch in text if ch.isprintable())

    # Normalizing whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

df['education'] = df['education'].apply(clean_text)
df['address'] = df['address'].apply(clean_text)
df['specializations']= df['specializations'].apply(clean_text)
df['biography'] = df['biography'].apply(clean_text)
df['research']=df['research'].apply(clean_text)


# %%
def clean_and_categorize_phone(phone):
    if not isinstance(phone, str) or not phone.strip():
        return None
    
    # Remove hyphens and spaces, then extract digit groups
    phone_cleaned = phone.replace("-", "").replace(" ", "")
    result = {"mobile": [], "landline": []}
    
    for num in re.findall(r"\d+", phone_cleaned):
        if len(num) == 10 and num[0] in "6789":
            result["mobile"].append(num)
        elif num.startswith("0") and 10 <= len(num) <= 12:
            result["landline"].append(num)
    
    result = {k: v for k, v in result.items() if v}
    return result if result else None

df['phone'] = df['phone'].apply(clean_and_categorize_phone)

# %%
def clean_list(lst):
    if not isinstance(lst, list):
        return None

    cleaned = [
        clean_text(item)
        for item in lst
        if isinstance(item, str) and clean_text(item)
    ]

    return cleaned if cleaned else None

df['teaching'] = df['teaching'].apply(clean_list)

# %%
def clean_publications(pub_list):
    """Merging broken publication fragments"""
    if not isinstance(pub_list, list):
        return None

    publications = []
    buffer = ""

    for item in pub_list:
        if not isinstance(item, str):
            continue

        item = clean_text(item)
        if not item:
            continue

        buffer += " " + item

        if re.search(r"\b(19|20)\d{2}\b", buffer) or "doi" in buffer.lower():
            publications.append(buffer.strip())
            buffer = ""

    if buffer.strip():
        publications.append(buffer.strip())

    return publications if publications else None

df["publications"] = df["publications"].apply(clean_publications)

# %%
def clean_links(links):
    if not isinstance(links, list):
        return None

    links = [l.strip() for l in links if isinstance(l, str) and l.startswith("http")]
    return links if links else None

df["website_links"] = df["website_links"].apply(clean_links)

# %%
def categorize_links(links):
    if not isinstance(links, list) or not links:
        return None

    categorized = {
        "personal_website": [],
        "google_scholar": [],
        "linkedin": [],
        "youtube": [],
        "other": []
    }

    for link in links:
        if "scholar.google" in link:
            categorized["google_scholar"].append(link)

        elif "linkedin.com" in link:
            categorized["linkedin"].append(link)

        elif "youtube.com" in link or "youtu.be" in link:
            categorized["youtube"].append(link)

        elif "sites.google" in link or "github.io" in link:
            categorized["personal_website"].append(link)

        else:
            categorized["other"].append(link)

    categorized = {k: v for k, v in categorized.items() if v}

    return categorized if categorized else None

df["website_links"] = df["website_links"].apply(categorize_links)


# %%
# normalizing all values including empty strings to None
df = df.applymap(
    lambda x: None if isinstance(x, str) and not x.strip() else x
)
df = df.where(pd.notnull(df), None)

# %%
df.to_csv(
    "../data/processed/faculty_cleaned.csv",
    index=False
)

print("Cleaning completed and saved to faculty_cleaned.csv")

# %%
df.head(5)

