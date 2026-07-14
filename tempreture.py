import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

prompt = "Explain Artificial Intelligence in simple words."

temperatures = [0.0, 0.3, 0.7, 1.0]

for temp in temperatures:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=temp,
        max_tokens=300,   # Increased from 150
    )

    print("=" * 60)
    print(f"Temperature: {temp}")
    print("=" * 60)

    if response.choices and response.choices[0].message.content:
        print(response.choices[0].message.content)
    else:
        print("No response received.")