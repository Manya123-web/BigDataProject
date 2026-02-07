import sqlite3
import os
import difflib
import faiss
import numpy as np

from pipeline.recommender.loader import get_all

def _calculate_keyword_score(query: str, faculty: dict) -> float:
    """
    Calculate keyword-based relevance score (0-1)
    Higher score = better match
    """
    query_lower = query.lower().strip()
    query_terms = query_lower.split()
    
    score = 0.0
    
    # Exact name match
    if faculty.get("name") and faculty["name"].lower() == query_lower:
        return 1.0
    
    # Partial name match
    if faculty.get("name") and query_lower in faculty["name"].lower():
        score = max(score, 0.95)
    
    # Topics match (primary field)
    if faculty.get("topics"):
        topics_lower = faculty["topics"].lower()
        terms_found = sum(1 for term in query_terms if term in topics_lower)
        if terms_found > 0:
            topics_score = 0.90 * (terms_found / len(query_terms)) if query_terms else 0.90
            score = max(score, topics_score)
    
    # Research match
    if faculty.get("research") and query_lower in faculty["research"].lower():
        score = max(score, 0.85)
    
    # Specializations match
    if faculty.get("specializations") and query_lower in faculty["specializations"].lower():
        score = max(score, 0.82)
    
    # Biography match
    if faculty.get("biography") and query_lower in faculty["biography"].lower():
        score = max(score, 0.78)
    
    return score


def search_faculty(query: str, k: int = 5):
    """
    Proper hybrid search: Semantic search + keyword extraction + ranking
    
    Process:
    1. Semantic search via FAISS embeddings (AI-powered)
    2. Keyword matching on results
    3. Combined scoring and ranking
    4. Return top-k best matches
    """
    
    model, index, metadata = get_all()

    print(f"\n🔍 Search Query: '{query}'")
    print(f"📊 Total Faculty: {len(metadata) if metadata else 0}")

    if not query or not query.strip():
        print("⚠️ Empty query - returning empty results")
        return []

    if not metadata or not model or index is None:
        print("❌ Missing model/index/metadata - trying database fallback")
        return _search_database_fallback(query, k)

    query_lower = query.lower().strip()

    # ============= STEP 1: Check for exact name matches =============
    exact_name_matches = [
        f for f in metadata
        if f.get("name") and f["name"].lower() == query_lower
    ]
    
    if exact_name_matches:
        print(f"✅ Exact name match found: {len(exact_name_matches)}")
        for f in exact_name_matches:
            f["similarity_score"] = 1.0
        return exact_name_matches[:k]

    # ============= STEP 2: Fuzzy name matching =============
    all_names = [f["name"] for f in metadata if f.get("name")]
    close_names = difflib.get_close_matches(query, all_names, n=1, cutoff=0.8)
    
    if close_names:
        fuzzy_matches = [f for f in metadata if f.get("name") in close_names]
        if fuzzy_matches:
            print(f"✅ Fuzzy name match found: {len(fuzzy_matches)}")
            for f in fuzzy_matches:
                f["similarity_score"] = 0.99
            return fuzzy_matches[:k]

    # ============= STEP 3: Semantic search using FAISS =============
    try:
        print("🧠 Performing semantic search via FAISS...")
        
        # Encode query to vector
        query_vec = model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_vec)
        
        # Search for more candidates than needed for reranking
        search_k = min(k * 15, len(metadata))
        distances, indices = index.search(query_vec, search_k)
        
        # FAISS with L2 normalization: lower distance = better match
        # Convert to similarity score (0-1, higher = better)
        semantic_results = []
        
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1 or idx >= len(metadata):
                continue
            
            faculty = metadata[idx].copy()
            
            # Convert L2 distance to similarity (lower distance = higher similarity)
            # Distance in [0, 2] for normalized vectors, convert to similarity in [0, 1]
            semantic_similarity = max(0, 1.0 - (distance / 2.0))
            faculty["semantic_score"] = float(semantic_similarity)
            
            # Calculate keyword score for same faculty
            keyword_score = _calculate_keyword_score(query, faculty)
            faculty["keyword_score"] = keyword_score
            
            # Combined score: 60% semantic + 40% keyword
            combined_score = (0.6 * semantic_similarity) + (0.4 * keyword_score)
            faculty["similarity_score"] = combined_score
            
            semantic_results.append(faculty)
        
        print(f"🔎 Found {len(semantic_results)} semantic candidates")
        
        if not semantic_results:
            print("❌ No semantic results - trying database fallback")
            return _search_database_fallback(query, k)
        
        # ============= STEP 4: Sort by combined score (best to low) =============
        semantic_results.sort(
            key=lambda x: x.get("similarity_score", 0),
            reverse=True  # Higher score first
        )
        
        print(f"✅ Top result: {semantic_results[0].get('name')} (score: {semantic_results[0].get('similarity_score'):.2f})")
        print(f"✨ Returning top {min(k, len(semantic_results))} results\n")
        
        return semantic_results[:k]
    
    except Exception as e:
        print(f"❌ Semantic search error: {e}")
        import traceback
        traceback.print_exc()
        return _search_database_fallback(query, k)


def _search_database_fallback(query: str, k: int = 5):
    """
    Fallback database search when FAISS unavailable
    """
    try:
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
            print("❌ Database not found")
            return []
        
        print(f"📚 Using database fallback: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query_lower = query.lower().strip()
        
        # Search with LIKE and order by relevance
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
            ORDER BY works_count DESC
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
                "similarity_score": 0.65
            }
            results.append(faculty)
        
        conn.close()
        print(f"📚 Database returned {len(results)} results')
        return results
        
    except Exception as e:
        print(f"❌ Database fallback error: {e}")
        import traceback
        traceback.print_exc()
        return []



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