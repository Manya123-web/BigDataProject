import pandas as pd

df = pd.read_csv("pipeline/data/processed/faculty_cleaned.csv")
n = len(df)

print("\n=== PROCESSED DATA OVERVIEW ===")
print(f"Total records: {n}")

print("\n=== TRUE MISSING VALUES (%) ===")
missing = (df.isnull().mean() * 100).round(1)
print(missing.sort_values(ascending=False))

print("\n=== KEY FIELD COVERAGE (%) ===")
key_fields = [
    "email",
    "phone",
    "education",
    "research",
    "publications",
    "website_links"
]

for col in key_fields:
    print(f"{col}: {round(df[col].notnull().mean() * 100, 1)}%")

print("\n=== RECORD COMPLETENESS ===")
row_completeness = df.notnull().mean(axis=1)
print("Average completeness:", round(row_completeness.mean() * 100, 1), "%")
print("Fully complete records:", (row_completeness == 1).sum())

print("\n=== PROCESSED DATA ===")
