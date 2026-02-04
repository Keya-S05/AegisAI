import json
from pathlib import Path
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

LOG_FILE = Path("logs/prompt_logs.json")

class OutputBehaviorMonitor:
    def __init__(self):
        self.embedder = pipeline(
            "feature-extraction",
            model="distilbert-base-uncased"
        )
        self.baseline_embeddings = self._load_baseline_embeddings()

    def _embed(self, text: str):
        # Shape: [tokens, hidden_dim]
        embedding = self.embedder(text)[0]
        embedding = np.array(embedding)

        # Mean pooling across tokens
        pooled_embedding = embedding.mean(axis=0)

        # Normalize to avoid cosine instability
        norm = np.linalg.norm(pooled_embedding)
        if norm == 0:
            return pooled_embedding

        return pooled_embedding / norm


    def _load_baseline_embeddings(self):
        if not LOG_FILE.exists():
            return []

        with open(LOG_FILE, "r") as f:
            data = json.load(f)

        embeddings = []
        for entry in data:
            output_text = entry["response"][0]["label"]
            embeddings.append(self._embed(output_text))

        return embeddings

    def check_output(self, output_text: str):
        if not self.baseline_embeddings:
            return {"output_anomaly": False, "similarity": 1.0}

        current_embedding = self._embed(output_text)

        similarities = cosine_similarity(
            [current_embedding],
            self.baseline_embeddings
        )
        avg_similarity = float(similarities.mean())

        return {
            "output_anomaly": bool(avg_similarity < 0.75),
            "similarity": avg_similarity
        }

