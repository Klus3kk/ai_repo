from transformers import pipeline

classifier = pipeline(task="sentiment-analysis")

prompt1 = "I think that I prefer to be alone."
prompt2 = "Come join us!"
prompt3 = "TO be or not to be? That is the question."

results = classifier([prompt1, prompt2, prompt3])

for result in results:
    print(f"label: {result['label']}, with score: {round(result['score'], 4)}")
