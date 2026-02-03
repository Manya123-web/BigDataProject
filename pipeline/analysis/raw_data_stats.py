import pandas as pd

df = pd.read_json("pipeline/data/raw/faculty_output.json")
n = len(df)

print("\n=== RAW DATA OVERVIEW ===")
print(f"Total records: {n}")

print("\n=== FIELD PRESENCE (%) ===")
presence = (df.notnull().mean() * 100).round(1)
print(presence)

print("\n=== EMPTY VALUES (%) ===")
empty = {}
for col in df.columns:
    empty[col] = round(
        (df[col].astype(str).str.strip().isin(["", "[]", "None"])).mean() * 100,
        1
    )
print(pd.Series(empty))

print("\n=== FIELDS THAT LOOK COMPLETE BUT ARE NOT ===")
for col in df.columns:
    if presence[col] == 100 and empty[col] > 20:
        print(f"{col}: {empty[col]}% empty")

print("\n=== RAW DATA ===")
