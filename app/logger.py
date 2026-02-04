import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/prompt_logs.json")

def log_event(prompt: str, response: dict):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response
    }

    # Ensure log file exists
    if not LOG_FILE.exists():
        LOG_FILE.parent.mkdir(exist_ok=True)
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Append log entry
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)

