# Code Sentry - AI Security Code Reviewer

Code Sentry is an AI-powered Python security code reviewer. It accepts a
security question and a source-code snippet, sends the request to a Gemini
LLM, and provides a structured security review.

The application also provides a local `scan_vulnerabilities` tool. The
Gemini model can automatically decide when the tool is needed, receive the
tool result, and incorporate the findings into its final response.

## Features

- AI-powered security code review
- Automatic function/tool calling
- Local static vulnerability scanner
- Structured security findings
- Severity levels and suggested fixes
- Plain-language security explanations
- Graceful handling of empty code
- Graceful handling of API/tool errors
- Unit tests for the local scanner

## Vulnerabilities Detected

The local scanner checks for:

1. Hardcoded secrets, credentials, and API keys
2. `eval()` and `exec()` usage
3. SQL queries constructed using string concatenation
4. SQL queries constructed using f-strings
5. `subprocess` calls using `shell=True`
6. Insecure `pickle.loads()` deserialization
7. Unsafe `yaml.load()` without `SafeLoader`
8. Weak hashing using MD5 or SHA-1
9. Potentially unvalidated user input

## Project Structure

```text
code_sentry/
├── main.py
├── tools.py
├── prompts.py
├── README.md
└── tests/
    └── test_tools.py