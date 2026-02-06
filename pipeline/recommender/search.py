from .loader import get_all
import faiss


def search_faculty(query: str, k: int = 5):
    """
    Hybrid faculty search:
    1️⃣ Exact name match (highest priority)
    2️⃣ Partial keyword match
    3️⃣ Semantic similarity via FAISS
    """

    model, index, metadata = get_all()

    if not query or not query.strip():
        return []

    query_lower = query.lower()

    # =====================================================
    # ⭐ STEP 1 — EXACT NAME MATCH (RETURN IMMEDIATELY)
    # =====================================================

    exact_matches = [
        f for f in metadata
        if f.get("name") and f["name"].lower() == query_lower
    ]

    if exact_matches:
        for faculty in exact_matches:
            faculty["similarity_score"] = 1.0   # perfect score
        return exact_matches[:k]

    # =====================================================
    # ⭐ STEP 2 — PARTIAL KEYWORD BOOST
    # =====================================================

    keyword_matches = [
        f for f in metadata
        if f.get("name") and query_lower in f["name"].lower()
    ]

    # =====================================================
    # ⭐ STEP 3 — SEMANTIC SEARCH
    # =====================================================

    query_vec = model.encode([query], convert_to_numpy=True)

    # cosine similarity
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, k * 3)
    # search more so we can merge + rank later

    semantic_results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        faculty = metadata[idx].copy()
        faculty["similarity_score"] = float(score)

        # Robustness: ensure we don't return broken metadata
        if not faculty.get("name"):
            continue

        semantic_results.append(faculty)

    # =====================================================
    # ⭐ STEP 4 — MERGE RESULTS (NO DUPLICATES)
    # =====================================================

    seen_ids = set()
    final_results = []

    # Keyword matches FIRST
    for faculty in keyword_matches:
        fid = faculty["id"]

        if fid not in seen_ids:
            faculty_copy = faculty.copy()
            faculty_copy["similarity_score"] = 0.9  # boosted
            final_results.append(faculty_copy)
            seen_ids.add(fid)

    # Then semantic
    for faculty in semantic_results:
        fid = faculty["id"]

        if fid not in seen_ids:
            final_results.append(faculty)
            seen_ids.add(fid)

    # =====================================================
    # ⭐ STEP 5 — SORT BY SCORE
    # =====================================================

    final_results.sort(
        key=lambda x: x.get("similarity_score", 0),
        reverse=True
    )

    return final_results[:k]
