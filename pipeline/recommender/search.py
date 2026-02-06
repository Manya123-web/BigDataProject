import sqlite3
import os
import difflib


def search_faculty(query: str, k: int = 5):
    """
    Hybrid faculty search with database fallback:
    1. Exact name match (highest priority)
    2. Partial keyword match
    3. Semantic similarity via FAISS
    4. Database fallback if FAISS fails
    """

    model, index, metadata = get_all()

    # Add debugging
    print(f" Search query: '{query}'")
    print(f" Total metadata entries: {len(metadata) if metadata else 0}")

    if not query or not query.strip():
        print(" Empty query received")
        return []

    # If metadata is not loaded, try database fallback
    if not metadata:
        print(" No metadata loaded! Trying database fallback...")
        return _search_database_fallback(query, k)

    query_lower = query.lower().strip()


    exact_matches = [
        f for f in metadata
        if f.get("name") and f["name"].lower().strip() == query_lower
    ]

    # Spelling mistake accountability for Name
    if not exact_matches:
        all_names = [f["name"] for f in metadata if f.get("name")]
        close_names = difflib.get_close_matches(query, all_names, n=3, cutoff=0.7)
        exact_matches = [
            f for f in metadata
            if f.get("name") in close_names
        ]

    if exact_matches:
        print(f" Found {len(exact_matches)} matches (Exact or Fuzzy Name)")
        for faculty in exact_matches:
            faculty["similarity_score"] = 1.0   # perfect score
        return exact_matches[:k]


    keyword_matches = [
        f for f in metadata
        if f.get("name") and query_lower in f["name"].lower()
    ]

    print(f" Found {len(keyword_matches)} keyword match(es) in names")

    # Also search in topics, research, specializations, and faculty_type
    content_matches = [
        f for f in metadata
        if (
            (f.get("topics") and query_lower in f["topics"].lower()) or
            (f.get("research") and query_lower in f["research"].lower()) or
            (f.get("specializations") and query_lower in f["specializations"].lower()) or
            (f.get("faculty_type") and query_lower in f["faculty_type"].lower())
        )
    ]

    # Check for spelling mistakes in faculty_type specifically
    if not content_matches:
        all_types = list(set(f["faculty_type"] for f in metadata if f.get("faculty_type")))
        close_types = difflib.get_close_matches(query, all_types, n=1, cutoff=0.8)
        if close_types:
            content_matches = [
                f for f in metadata
                if f.get("faculty_type") == close_types[0]
            ]

    print(f"Found {len(content_matches)} keyword/fuzzy matches in content/type")



    try:
        query_vec = model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_vec)

        # Search more results to merge later
        search_k = min(k * 5, len(metadata))
        scores, indices = index.search(query_vec, search_k)

        semantic_results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(metadata):
                continue

            faculty = metadata[idx].copy()
            faculty["similarity_score"] = float(score)

            # Ensure we have a valid name
            if not faculty.get("name"):
                continue

            semantic_results.append(faculty)

        print(f" Found {len(semantic_results)} semantic match(es)")

    except Exception as e:
        print(f" Semantic search error: {e}")
        semantic_results = []

    seen_ids = set()
    final_results = []

    # Priority 1: Name keyword matches
    for faculty in keyword_matches:
        fid = faculty["id"]
        if fid not in seen_ids:
            faculty_copy = faculty.copy()
            faculty_copy["similarity_score"] = 0.95  # high boost
            final_results.append(faculty_copy)
            seen_ids.add(fid)

    # Priority 2: Content keyword matches
    for faculty in content_matches:
        fid = faculty["id"]
        if fid not in seen_ids:
            faculty_copy = faculty.copy()
            faculty_copy["similarity_score"] = 0.85  # medium boost
            final_results.append(faculty_copy)
            seen_ids.add(fid)

    # Priority 3: Semantic matches
    for faculty in semantic_results:
        fid = faculty["id"]
        if fid not in seen_ids:
            # Ensure we are passing along ALL metadata from the faculty object
            final_results.append(faculty.copy())
            seen_ids.add(fid)


    final_results.sort(
        key=lambda x: x.get("similarity_score", 0),
        reverse=True
    )

    print(f" Returning {len(final_results[:k])} results")
    
    # If no results found, try database fallback
    if len(final_results) == 0:
        print(" No results from FAISS search, trying database fallback...")
        return _search_database_fallback(query, k)
    
    return final_results[:k]


def _search_database_fallback(query: str, k: int = 5):
    """
    Fallback to direct database search when FAISS is unavailable or returns no results
    """
    try:
        # Try different possible database paths
        possible_db_paths = [
            "pipeline/outputs/faculty.db",
            "outputs/faculty.db",
            "../outputs/faculty.db",
        ]
        
        db_path = None
        for path in possible_db_paths:
            if os.path.exists(path):
                db_path = path
                break
        
        if not db_path:
            print(" Database not found in any expected location")
            return []
        
        print(f"Using database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query_lower = query.lower().strip()
        
        # Search in name, research, topics, specializations, faculty_type
        cursor.execute("""
            SELECT 
                id, name, faculty_type, education, research, 
                specializations, teaching, email, image_url, 
                works_count, topics, phone, address, publications, website_links
            FROM faculty
            WHERE 
                LOWER(name) LIKE ? OR
                LOWER(research) LIKE ? OR
                LOWER(topics) LIKE ? OR
                LOWER(specializations) LIKE ? OR
                LOWER(faculty_type) LIKE ?
            LIMIT ?
        """, (f"%{query_lower}%", f"%{query_lower}%", f"%{query_lower}%", f"%{query_lower}%", f"%{query_lower}%", k))
        
        results = []
        for row in cursor.fetchall():
            faculty = {
                "id": row[0],
                "name": row[1],
                "faculty_type": row[2],
                "education": row[3],
                "research": row[4],
                "specializations": row[5],
                "teaching": row[6],
                "email": row[7],
                "image_url": row[8],
                "works_count": row[9],
                "topics": row[10],
                "phone": row[11],
                "address": row[12],
                "publications": row[13],
                "website_links": row[14],
                "similarity_score": 0.75 
            }
            results.append(faculty)
        
        conn.close()
        print(f"Database fallback returned {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Database fallback error: {e}")
        import traceback
        traceback.print_exc()
        return []