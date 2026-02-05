from sentence_transformers import SentenceTransformer
import faiss
import pickle
import torch

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

model = None
index = None
metadata = None


def load_all():

    global model, index, metadata

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"\nLoading transformer on {device}...")
    model = SentenceTransformer(MODEL_NAME, device=device)

    print("Loading FAISS index...")
    index = faiss.read_index("pipeline/data/faiss.index")

    print("Loading metadata...")
    with open("pipeline/data/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    print("✅ Recommender ready!\n")


def get_all():
    return model, index, metadata
