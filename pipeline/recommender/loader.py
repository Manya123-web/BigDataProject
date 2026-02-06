import sys
import os
# Add user site-packages explicitly to fix import errors
user_site = r"C:\Users\tcpladmin255\AppData\Roaming\Python\Python312\site-packages"
if user_site not in sys.path and os.path.exists(user_site):
    sys.path.append(user_site)

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
