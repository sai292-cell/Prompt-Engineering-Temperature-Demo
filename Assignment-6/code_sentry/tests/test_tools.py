import unittest

from tools import scan_vulnerabilities


class TestScanVulnerabilities(unittest.TestCase):

    def test_hardcoded_secret(self):
        code = 'api_key = "123456789abcdef"'

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("Hardcoded Secret", categories)

    def test_eval(self):
        code = "result = eval(user_input)"

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("Dynamic Code Execution", categories)

    def test_sql_injection(self):
        code = 'query = "SELECT * FROM users WHERE name = " + name'

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("SQL Injection", categories)

    def test_shell_true(self):
        code = 'subprocess.run(command, shell=True)'

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("Command Injection", categories)

    def test_pickle(self):
        code = "data = pickle.loads(user_data)"

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("Insecure Deserialization", categories)

    def test_md5(self):
        code = "hashlib.md5(password.encode())"

        result = scan_vulnerabilities(code)

        categories = [
            finding["category"]
            for finding in result["findings"]
        ]

        self.assertIn("Weak Hashing", categories)

    def test_clean_code(self):
        code = """
def add_numbers(a, b):
    return a + b
"""

        result = scan_vulnerabilities(code)

        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()