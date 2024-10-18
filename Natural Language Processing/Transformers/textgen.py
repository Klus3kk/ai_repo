from transformers import pipeline

generator = pipeline(task="text-generation", model="gpt2")

prompt = "In the future I want to become"

output = generator(prompt, max_length=50, num_return_sequences=1)

print("\n\n\n\n\n")

print(output[0]['generated_text'])
