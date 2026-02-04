import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest

LOG_FILE = Path("logs/prompt_logs.json")

class InputAnomalyDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500
        )
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self._train_model()

    def _load_prompts(self):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
        return [entry["prompt"] for entry in data]

    def _train_model(self):
        prompts = self._load_prompts()
        vectors = self.vectorizer.fit_transform(prompts)
        self.model.fit(vectors)

    def score_prompt(self, prompt: str):
        vector = self.vectorizer.transform([prompt])
        score = self.model.decision_function(vector)[0]

        # Security-aware threshold
        THRESHOLD = 0.15
        is_anomaly = score < THRESHOLD

        return {
            "anomaly_score": float(score),
            "is_anomaly": bool(is_anomaly)
        }


