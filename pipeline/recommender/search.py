import sqlite3
import os
import difflib
import faiss
import numpy as np

from pipeline.recommender.loader import get_all

def hybrid_search_rerank(query: str, candidates: list, model) -> list:
    """
    Hybrid candidate filtering + semantic reranking
    
    Combines:
    1. Exact match (score 1.0)
    2. Keyword match in primary fields (name, topics) (score 0.90-0.95)
    3. Keyword match in secondary fields (research, specializations) (score 0.78-0.85)
    4. Semantic similarity scores (from FAISS)
    
    Returns candidates sorted by combined score, with deduplication
    """
    
    if not query.strip() or not candidates:
        return candidates
    
    query_lower = query.lower().strip()
    query_terms = query_lower.split()
    
    exact_matches = []
    keyword_matches = []
    semantic_matches = []
    
    for faculty in candidates:
        match_type = None
        relevance_score = 0
        
        # Priority 1: Exact name match
        if faculty.get("name") and faculty["name"].lower() == query_lower:
            faculty_copy = faculty.copy()
            faculty_copy["_hybrid_score"] = 1.0
            faculty_copy["_match_type"] = "exact_name"
            exact_matches.append(faculty_copy)
            continue
        
        # Priority 2: Keyword match in primary fields (name, topics)
        primary_field_score = 0
        
        # Name contains query
        if faculty.get("name") and query_lower in faculty["name"].lower():
            primary_field_score = 0.95
            keyword_matches.append({
                "faculty": faculty.copy(),
                "score": primary_field_score,
                "field": "name"
            })
            continue
        
        # Multiple keywords in topics
        if faculty.get("topics"):
            topics_lower = faculty["topics"].lower()
            terms_found = sum(1 for term in query_terms if term in topics_lower)
            if terms_found > 0:
                topics_score = 0.90 * (terms_found / len(query_terms)) if query_terms else 0.90
                keyword_matches.append({
                    "faculty": faculty.copy(),
                    "score": topics_score,
                    "field": "topics"
                })
                continue
        
        # Priority 3: Keyword match in secondary fields
        secondary_field_score = 0
        
        if faculty.get("research") and query_lower in faculty["research"].lower():
            secondary_field_score = max(secondary_field_score, 0.85)
        
        if faculty.get("specializations") and query_lower in faculty["specializations"].lower():
            secondary_field_score = max(secondary_field_score, 0.82)
        
        if faculty.get("biography") and query_lower in faculty["biography"].lower():
            secondary_field_score = max(secondary_field_score, 0.78)
        
        if secondary_field_score > 0:
            keyword_matches.append({
                "faculty": faculty.copy(),
                "score": secondary_field_score,
                "field": "secondary"
            })
            continue
        
        # Priority 4: Use semantic similarity score
        if faculty.get("similarity_score") and faculty["similarity_score"] > 0.5:
            faculty_copy = faculty.copy()
            faculty_copy["_hybrid_score"] = faculty["similarity_score"]
            faculty_copy["_match_type"] = "semantic"
            semantic_matches.append(faculty_copy)
    
    # Combine results in priority order
    combined_results = (
        exact_matches +
        [m["faculty"] for m in sorted(keyword_matches, key=lambda x: x["score"], reverse=True)] +
        semantic_matches
    )
    
    # Remove duplicates (keep first/best occurrence)
    seen_ids = set()
    deduped = []
    
    for faculty in combined_results:
        fid = faculty.get("id")
        if fid and fid not in seen_ids:
            # Set hybrid score if not already set
            if "_hybrid_score" not in faculty:
                faculty["_hybrid_score"] = faculty.get("similarity_score", 0.5)
            deduped.append(faculty)
            seen_ids.add(fid)
    
    # Final sort by combined score
    deduped.sort(
        key=lambda x: x.get("_hybrid_score", x.get("similarity_score", 0)),
        reverse=True
    )
    
    return deduped


def search_faculty(query: str, k: int = 5):
    """
    Hybrid faculty search with semantic reranking:
    1. Load FAISS index and embeddings
    2. Perform semantic search
    3. Apply hybrid filtering + reranking
    4. Return top-k results
    """

    model, index, metadata = get_all()

    print(f"\n🔍 Search query: '{query}'")
    print(f"📊 Total metadata entries: {len(metadata) if metadata else 0}")

    if not query or not query.strip():
        print("⚠️ Empty query received")
        return []

    # If metadata is not loaded, try database fallback
    if not metadata:
        print("❌ No metadata loaded! Trying database fallback...")
        return _search_database_fallback(query, k)

    query_lower = query.lower().strip()

    # Step 1: Exact name match (highest priority)
    exact_matches = [
        f for f in metadata
        if f.get("name") and f["name"].lower().strip() == query_lower
    ]

    # Fuzzy name matching
    if not exact_matches:
        all_names = [f["name"] for f in metadata if f.get("name")]
        close_names = difflib.get_close_matches(query, all_names, n=3, cutoff=0.7)
        exact_matches = [
            f for f in metadata
            if f.get("name") in close_names
        ]

    if exact_matches:
        print(f"✅ Found {len(exact_matches)} exact/fuzzy name matches")
        for faculty in exact_matches:
            faculty["similarity_score"] = 1.0
        return exact_matches[:k]

    # Step 2: Semantic search with FAISS
    try:
        query_vec = model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_vec)

        # Search more results for hybrid filtering
        search_k = min(k * 10, len(metadata))
        scores, indices = index.search(query_vec, search_k)

        semantic_candidates = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(metadata):
                continue

            faculty = metadata[idx].copy()
            faculty["similarity_score"] = float(score)

            if not faculty.get("name"):
                continue

            semantic_candidates.append(faculty)

        print(f"🔎 Found {len(semantic_candidates)} semantic candidates")

    except Exception as e:
        print(f"⚠️ Semantic search error: {e}")
        semantic_candidates = []

    # If no semantic results, fallback
    if not semantic_candidates:
        print("📚 No semantic results, trying database fallback...")
        return _search_database_fallback(query, k)

    # Step 3: Apply hybrid filtering + semantic reranking
    print(f"🎯 Applying hybrid filtering + semantic reranking...")
    reranked_results = hybrid_search_rerank(query, semantic_candidates, model)

    print(f"✨ Returning top {min(k, len(reranked_results))} results")
    
    return reranked_results[:k]


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