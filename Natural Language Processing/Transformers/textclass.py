from transformers import pipeline

classifier = pipeline(task="sentiment-analysis")

prompt1 = "I think that I prefer to be alone."
prompt2 = "Come join us!"

results = classifier([])

print(classifier(prompt))
