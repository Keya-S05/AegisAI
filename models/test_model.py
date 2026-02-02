from transformers import pipeline

print("Loading AI model...")
classifier = pipeline("sentiment-analysis")

text = "This is a cybersecurity project for AI anomaly detection."
result = classifier(text)

print("Input Text:", text)
print("Model Output:", result)

