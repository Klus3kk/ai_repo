from transformers import pipeline

classifier = pipeline(task="sentiment-analysis")

prompt = "I think that I prefer to be alone."

print(classifier(prompt))
