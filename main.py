from fastapi import FastAPI
from pydantic import BaseModel
from models.ai_model import AIModel

app = FastAPI(
    title="AegisAI",
    description="Cybersecurity-based anomaly detection system for AI models",
    version="0.1"
)

# Load model once at startup
ai_model = AIModel()

class PromptRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "AegisAI API running"}

@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    result = ai_model.analyze(request.text)
    return {
        "input": request.text,
        "analysis": result
    }

