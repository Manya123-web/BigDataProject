import sqlite3
import os

DB_PATH = "pipeline/outputs/faculty.db"

def check():
    if not os.path.exists(DB_PATH):
        print(f"Error: DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("--- Table Info ---")
    cursor.execute("PRAGMA table_info(faculty)")
    for info in cursor.fetchall():
        print(info)
        
    print("\n--- Row Counts ---")
    cursor.execute("SELECT COUNT(*) FROM faculty")
    print(f"Total rows: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(works_count) FROM faculty WHERE works_count IS NOT NULL")
    print(f"Rows with works_count: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT SUM(works_count) FROM faculty")
    print(f"Total works_count: {cursor.fetchone()[0]}")
    
    print("\n--- Sample Rows (works_count) ---")
    cursor.execute("SELECT name, works_count FROM faculty LIMIT 5")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    check()
