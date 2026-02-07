from pipeline.recommender.search import search_faculty
try:
    results = search_faculty("machine learning", k=1)
    print("Search successful!")
    print(f"Results found: {len(results)}")
except NameError as e:
    print(f"FAILED: {e}")
except Exception as e:
    print(f"ERROR: {e}")
