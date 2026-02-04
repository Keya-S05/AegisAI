from fastapi import FastAPI
from pydantic import BaseModel
from models.ai_model import AIModel
from app.logger import log_event
from app.anomaly_detector import InputAnomalyDetector
from app.output_monitor import OutputBehaviorMonitor

app = FastAPI(
    title="AegisAI",
    description="Cybersecurity-based anomaly detection system for AI models",
    version="0.1"
)

# Load model once at startup
ai_model = AIModel()
anomaly_detector = InputAnomalyDetector()
output_monitor = OutputBehaviorMonitor()

class PromptRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "AegisAI API running"}

@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    analysis = ai_model.analyze(request.text)
    anomaly = anomaly_detector.score_prompt(request.text)

    output_text = analysis[0]["label"]
    output_check = output_monitor.check_output(output_text)

    log_event(request.text, analysis)

    return {
        "input": request.text,
        "analysis": analysis,
        "input_anomaly": anomaly,
        "output_behavior": output_check
    }

