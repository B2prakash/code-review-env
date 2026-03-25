TASKS = {
    "task_1": {
        "id": "task_1",
        "name": "Bug Identification",
        "difficulty": "easy",
        "description": "Review this Python code and identify the bugs.",
        "language": "python",
        "code_diff": """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers) + 1):  # Bug: off-by-one error
        total += numbers[i]
    return total / len(numbers)

def get_user_data(user_id):
    users = {1: "Alice", 2: "Bob"}
    return users[user_id].upper()  # Bug: no None/key check
""",
        "expected_issues": [
            "off-by-one",
            "index error",
            "key error",
            "none",
            "missing check"
        ],
        "expected_severity": "high",
        "max_turns": 5
    },

    "task_2": {
        "id": "task_2",
        "name": "Security Audit",
        "difficulty": "medium",
        "description": "Review this Flask route for security vulnerabilities.",
        "language": "python",
        "code_diff": """
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Bug 1: SQL injection vulnerability
    conn = sqlite3.connect('users.db')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchone()
    
    # Bug 2: No authentication check on result
    return {"status": "success", "user": result}
""",
        "expected_issues": [
            "sql injection",
            "authentication",
            "parameterized",
            "input validation",
            "security"
        ],
        "expected_severity": "high",
        "max_turns": 5
    },

    "task_3": {
        "id": "task_3",
        "name": "Refactor Quality Review",
        "difficulty": "hard",
        "description": "Review this refactored code for quality issues, performance problems, and broken edge cases.",
        "language": "python",
        "code_diff": """
# Original: simple list search
# Refactored version below - review for issues

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.cache = {}
    
    def process(self, items):
        results = []
        for item in items:
            # Bug 1: Performance - calling expensive operation in loop
            processed = self._expensive_transform(item)
            results.append(processed)
        return results
    
    def _expensive_transform(self, item):
        # Bug 2: Cache never used properly
        if item in self.cache:
            return self.cache[item]
        result = item * 2
        # Bug 3: Cache grows forever - no size limit
        self.cache[item] = result
        return result
    
    def get_summary(self, items):
        # Bug 4: Returns wrong type for empty list
        if not items:
            return None  # Should return empty dict
        return {
            "count": len(items),
            "total": sum(items),
            # Bug 5: Division without zero check
            "average": sum(items) / len(items)
        }
""",
        "expected_issues": [
            "performance",
            "cache",
            "memory leak",
            "edge case",
            "empty list",
            "division"
        ],
        "expected_severity": "medium",
        "max_turns": 8
    }
}