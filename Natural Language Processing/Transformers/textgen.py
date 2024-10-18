# from transformers import pipeline

# generator = pipeline(task="text-generation", model="gpt2")

# prompt = "In the future I want to become"

# output = generator(prompt, max_length=50, num_return_sequences=1)

# print("\n\n\n\n\n")

# print(output[0]['generated_text'])


# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
pipe(messages)