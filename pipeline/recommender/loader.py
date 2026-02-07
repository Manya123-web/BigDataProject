import sys
import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import torch

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

model = None
index = None
metadata = None


def load_all():
    """Load the model, FAISS index, and metadata"""
    global model, index, metadata

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"\n🚀 Loading transformer on {device}...")
        model = SentenceTransformer(MODEL_NAME, device=device)

        # Try different possible paths (Search directory relative to execution)
        # Try different possible paths (Search directory relative to execution)
        base_dir = os.path.dirname(os.path.abspath(__file__)) # pipeline/recommender
        root_dir = os.path.dirname(os.path.dirname(base_dir)) # Project root

        possible_paths = [
            (os.path.join(base_dir, "data", "faiss.index"), os.path.join(base_dir, "data", "metadata.pkl")),
            ("pipeline/recommender/data/faiss.index", "pipeline/recommender/data/metadata.pkl"),
            ("data/faiss.index", "data/metadata.pkl"),
        ]

        index_loaded = False
        for index_path, meta_path in possible_paths:
            if os.path.exists(index_path) and os.path.exists(meta_path):
                print(f"📂 Loading FAISS index from: {index_path}")
                index = faiss.read_index(index_path)

                print(f"📂 Loading metadata from: {meta_path}")
                with open(meta_path, "rb") as f:
                    metadata = pickle.load(f)

                print(f"✅ Loaded {len(metadata)} faculty records")
                print(f"✅ FAISS index dimension: {index.d}")
                print(f"✅ FAISS index total vectors: {index.ntotal}")
                
                index_loaded = True
                break

        if not index_loaded:
            print("❌ ERROR: Could not find FAISS index or metadata!")
            print("Searched in:")
            for idx_path, _ in possible_paths:
                print(f"  - {os.path.abspath(idx_path)}")
            print("\n⚠️ Please run build_index.py first!")
            
            # Initialize empty to prevent crashes
            metadata = []
            index = None

        print("✅ Recommender ready!\n")

    except Exception as e:
        print(f"❌ Error loading recommender: {e}")
        import traceback
        traceback.print_exc()
        
        # Initialize empty to prevent crashes
        metadata = []
        index = None


def get_all():
    """Get the loaded model, index, and metadata"""
    if model is None or index is None or metadata is None:
        print("⚠️ Recommender not loaded, attempting to load now...")
        load_all()
    
    return model, index, metadata