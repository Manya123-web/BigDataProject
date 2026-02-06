import sqlite3
import requests
import json
import time

DB_PATH = "../outputs/faculty.db"

def enrich_faculty():
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all faculty to enrich
    cursor.execute("SELECT id, name FROM faculty WHERE openalex_id IS NULL")
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
                    
                    print(f"  -> Match found! Works: {works_count}, Topics: {topics_str}")
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
