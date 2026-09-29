import os

from google import genai
from google.genai import types

from tools import scan_vulnerabilities
from prompts import SYSTEM_PROMPT


def create_client():
    """Create the Gemini API client."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    return genai.Client(api_key=api_key)


def review_code(query: str, code: str, language: str = ""):
    """Review code using Gemini and automatic function calling."""

    client = create_client()

    user_prompt = f"""
User security question:
{query}

Programming language:
{language or "Not specified"}

Code snippet:
{code}
"""

    try:
        chat = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[scan_vulnerabilities],
            ),
        )

        response = chat.send_message(user_prompt)

        return response.text

    except Exception as exc:
        return (
            "Security review could not be completed.\n"
            f"Error: {exc}"
        )


def main():
    print("=" * 60)
    print("        CODE SENTRY - AI SECURITY CODE REVIEWER")
    print("=" * 60)

    query = input(
        "\nEnter your security question:\n> "
    ).strip()

    language = input(
        "\nEnter programming language (optional):\n> "
    ).strip()

    print(
        "\nPaste your code below."
        "\nType END on a separate line when finished."
    )

    code_lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        code_lines.append(line)

    code = "\n".join(code_lines)

    if not code.strip():
        print("\nNo code was provided.")
        return

    print("\nAnalyzing code...\n")

    result = review_code(
        query=query,
        code=code,
        language=language
    )

    print("=" * 60)
    print("SECURITY REVIEW")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()