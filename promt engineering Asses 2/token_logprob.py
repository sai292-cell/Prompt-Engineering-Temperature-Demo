import math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from colorama import Fore, Style, init

init(autoreset=True)

MODEL_NAME = "distilgpt2"

print("Loading model (first run may take a minute)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

prompt = input("Enter your prompt: ")

inputs = tokenizer(prompt, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits
log_probs = torch.nn.functional.log_softmax(logits, dim=-1)

input_ids = inputs["input_ids"][0]

print("\n" + "=" * 90)
print(f"{'Token':20} {'Log Probability':15} {'Probability':15} {'Cumulative'}")
print("=" * 90)

colors = [
    Fore.GREEN,
    Fore.YELLOW,
    Fore.RED,
    Fore.CYAN,
    Fore.MAGENTA,
    Fore.BLUE
]

cumulative_probability = 1.0

for i in range(1, len(input_ids)):
    token_id = input_ids[i]
    token = tokenizer.decode(token_id)

    logprob = log_probs[0, i - 1, token_id].item()
    probability = math.exp(logprob)

    cumulative_probability *= probability

    color = colors[i % len(colors)]

    print(
        color +
        f"{token:20}"
        f"{logprob:<15.6f}"
        f"{probability:<15.6f}"
        f"{cumulative_probability:.10f}"
    )

print(Style.RESET_ALL)

print("\nGenerated Response:\n")

generated = model.generate(
    **inputs,
    max_new_tokens=40,
    do_sample=True,
    temperature=0.7
)

print(tokenizer.decode(generated[0], skip_special_tokens=True))