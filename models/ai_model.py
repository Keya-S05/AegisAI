from transformers import pipeline

class AIModel:
    def __init__(self):
        print("Loading AI model...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def analyze(self, text: str):
        return self.classifier(text)

