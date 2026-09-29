import re


def scan_vulnerabilities(code: str, language: str = "") -> dict:
    """
    Scan source code for common security vulnerabilities.

    Args:
        code: Source code to scan.
        language: Optional programming language hint.

    Returns:
        Dictionary containing vulnerability findings.
    """

    findings = []

    if not code or not code.strip():
        return {
            "findings": [],
            "message": "No code was provided for scanning."
        }

    lines = code.splitlines()

    def add_finding(category, severity, line_number, description, fix):
        findings.append({
            "category": category,
            "severity": severity,
            "line": line_number,
            "description": description,
            "suggested_fix": fix
        })

    # ---------------------------------------------------------
    # 1. Hardcoded secrets / API keys
    # ---------------------------------------------------------

    secret_pattern = re.compile(
        r'(?i)\b(api[_-]?key|secret[_-]?key|password|passwd|'
        r'token|access[_-]?token|auth[_-]?token)\b'
        r'\s*[:=]\s*["\'][^"\']+["\']'
    )

    for line_number, line in enumerate(lines, start=1):
        if secret_pattern.search(line):
            add_finding(
                "Hardcoded Secret",
                "High",
                line_number,
                "A possible password, token, API key, or secret is hardcoded in the source code.",
                "Move secrets to environment variables or a secure secret manager."
            )

    # ---------------------------------------------------------
    # 2. eval() / exec()
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"\beval\s*\(", line):
            add_finding(
                "Dynamic Code Execution",
                "High",
                line_number,
                "eval() can execute dynamically supplied Python code.",
                "Avoid eval(). Use safe parsing or explicit validation instead."
            )

        if re.search(r"\bexec\s*\(", line):
            add_finding(
                "Dynamic Code Execution",
                "High",
                line_number,
                "exec() can execute dynamically supplied Python code.",
                "Avoid exec(). Replace dynamic execution with safer logic."
            )

    # ---------------------------------------------------------
    # 3. SQL injection
    # ---------------------------------------------------------

    sql_keywords = re.compile(
        r"(?i)\b(select|insert|update|delete|replace)\b"
    )

    for line_number, line in enumerate(lines, start=1):

        if sql_keywords.search(line):

            # String concatenation
            if "+" in line:

                add_finding(
                    "SQL Injection",
                    "High",
                    line_number,
                    "A SQL statement appears to be constructed using string concatenation.",
                    "Use parameterized queries or prepared statements instead of concatenating user input."
                )

            # f-string SQL
            elif re.search(r'\bf["\']', line):

                add_finding(
                    "SQL Injection",
                    "High",
                    line_number,
                    "A SQL statement appears to use an f-string and may include untrusted input.",
                    "Use parameterized queries or prepared statements."
                )

            # % formatting
            elif "%" in line:

                add_finding(
                    "SQL Injection",
                    "High",
                    line_number,
                    "A SQL statement appears to be constructed using string formatting.",
                    "Use parameterized queries or prepared statements."
                )

    # ---------------------------------------------------------
    # 4. subprocess shell=True
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"\bshell\s*=\s*True\b", line):

            add_finding(
                "Command Injection",
                "High",
                line_number,
                "subprocess is being used with shell=True, which can enable command injection when input is untrusted.",
                "Avoid shell=True and pass command arguments as a list."
            )

    # ---------------------------------------------------------
    # 5. pickle.loads
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"\bpickle\.loads\s*\(", line):

            add_finding(
                "Insecure Deserialization",
                "High",
                line_number,
                "pickle.loads() can execute malicious code when loading untrusted data.",
                "Do not deserialize untrusted pickle data. Use a safer format such as JSON."
            )

    # ---------------------------------------------------------
    # 6. Unsafe yaml.load
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"\byaml\.load\s*\(", line):

            if "SafeLoader" not in line:

                add_finding(
                    "Insecure YAML Deserialization",
                    "High",
                    line_number,
                    "yaml.load() may deserialize unsafe YAML content.",
                    "Use yaml.safe_load() or yaml.SafeLoader."
                )

    # ---------------------------------------------------------
    # 7. Weak hashing
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"(?i)\b(md5|sha1)\b", line):

            add_finding(
                "Weak Hashing",
                "Medium",
                line_number,
                "MD5 or SHA-1 is weak and should not be used for password security.",
                "Use Argon2, bcrypt, scrypt, or PBKDF2 for password hashing."
            )

    # ---------------------------------------------------------
    # 8. Potentially unvalidated user input
    # ---------------------------------------------------------

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"\binput\s*\(", line):

            add_finding(
                "Potentially Unvalidated Input",
                "Medium",
                line_number,
                "User-controlled input is accepted and may require validation before being used in sensitive operations.",
                "Validate and constrain user input before using it."
            )

    return {
        "findings": findings,
        "message": (
            f"Scan completed. {len(findings)} potential issue(s) found."
            if findings
            else "Scan completed. No obvious vulnerabilities were detected."
        )
    }