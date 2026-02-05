from sentence_transformers import SentenceTransformer
import torch

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading model on {device}...")

model = SentenceTransformer(MODEL_NAME, device=device)

def get_model():
    return model
