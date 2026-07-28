import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

prompt = input("Enter your prompt: ")

models = {
    "Base Model": "meta-llama/llama-3.1-8b",
    "Instruct Model": "meta-llama/llama-3.1-8b-instruct",
}

for name, model in models.items():
    print("\n" + "=" * 60)
    print(f"{name} ({model})")
    print("=" * 60)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
        )

        print(response.choices[0].message.content)

    except Exception as e:
        print("Error:", e)