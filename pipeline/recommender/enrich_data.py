import sqlite3
import requests
import json
import time

import os

# Set DB_PATH relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "outputs", "faculty.db")

def enrich_faculty():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all faculty to enrich (those without openalex_id OR without publications)
    cursor.execute("SELECT id, name FROM faculty WHERE openalex_id IS NULL OR publications IS NULL")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} faculty members to enrich.")

    for row in rows:
        fid, name = row
        print(f"Searching OpenAlex for: {name}...")

        try:
            # Clean name for search
            clean_name = name.split(',')[0] if ',' in name else name
            
            # API Call
            url = f"https://api.openalex.org/authors?search={clean_name}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if results:
                    # Take the top result
                    top_match = results[0]
                    
                    openalex_id = top_match.get("id")
                    works_count = top_match.get("works_count", 0)
                    
                    # Extract topics (top 3)
                    topics_list = [t['display_name'] for t in top_match.get("topics", [])[:3]]
                    topics_str = ", ".join(topics_list)

                    # Update DB (removed citations field)
                    cursor.execute("""
                        UPDATE faculty 
                        SET openalex_id = ?, works_count = ?, topics = ?
                        WHERE id = ?
                    """, (openalex_id, works_count, topics_str, fid))

                    # Fetch Works
                    print(f"  -> Fetching works for {openalex_id}...")
                    works_url = f"https://api.openalex.org/works?filter=author.id:{openalex_id}&sort=cited_by_count:desc&per_page=10"
                    works_response = requests.get(works_url)
                    if works_response.status_code == 200:
                        works_data = works_response.json()
                        works_list = [w.get("title") for w in works_data.get("results", []) if w.get("title")]
                        if works_list:
                            cursor.execute("""
                                UPDATE faculty 
                                SET publications = ?
                                WHERE id = ?
                            """, (json.dumps(works_list, ensure_ascii=False), fid))
                            print(f"  -> {len(works_list)} works found and saved.")
                    
                    print(f"  -> Match found! Works Count: {works_count}, Topics: {topics_str}")
                else:
                    print("  -> No match found in OpenAlex.")
            else:
                print(f"  -> API Error: {response.status_code}")

        except Exception as e:
            print(f"  -> Error: {e}")
        
        # Be nice to the API
        time.sleep(0.1)

    conn.commit()
    conn.close()
    print("Enrichment complete!")

if __name__ == "__main__":
    enrich_faculty()
