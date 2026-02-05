import sqlite3
import faiss
import pickle
import os

from model import get_model

DB_PATH = "outputs/faculty.db"
INDEX_PATH = "data/faiss.index"
IDS_PATH = "data/faculty_ids.pkl"
META_PATH = "data/metadata.pkl"


def fetch_faculty():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            faculty_type,
            name,
            education,
            specializations,
            biography,
            research,
            teaching,
            publications
        FROM faculty
    """)

    rows = cursor.fetchall()
    conn.close()

    faculty_ids = []
    faculty_texts = []
    metadata = []

    for row in rows:
        (
            fid,
            faculty_type,
            name,
            education,
            specializations,
            biography,
            research,
            teaching,
            publications
        ) = row

        combined = f"""
        Faculty Name: {name or ""}

        Faculty Type: {faculty_type or ""}

        Education:
        {education or ""}

        Research Interests:
        {research or ""}

        Areas of Specialization:
        {specializations or ""}

        Courses Taught:
        {teaching or ""}

        Publications:
        {publications or ""}

        Biography:
        {biography or ""}
        """

        faculty_ids.append(fid)
        faculty_texts.append(combined)

        metadata.append({
            "id": fid,
            "name": name,
            "faculty_type": faculty_type,
            "research": research,
            "specializations": specializations,
            "teaching": teaching
        })

    return faculty_ids, faculty_texts, metadata


def build_index():

    print("Fetching faculty data...")
    ids, texts, metadata = fetch_faculty()

    print("Loading transformer model...")
    model = get_model()

    print("Generating embeddings (GPU will be used if available)...")

    embeddings = model.encode(
        texts,
        batch_size=64,   # increase if GPU strong
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("Normalizing embeddings for cosine similarity...")
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(dim)  # cosine similarity
    index.add(embeddings)

    os.makedirs("data", exist_ok=True)

    print("Saving index + metadata...")
    faiss.write_index(index, INDEX_PATH)

    with open(IDS_PATH, "wb") as f:
        pickle.dump(ids, f)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("\n✅ FAISS index built successfully!")
    print(f"Total faculty indexed: {len(ids)}")


if __name__ == "__main__":
    build_index()
