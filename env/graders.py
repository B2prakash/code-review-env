from typing import Dict

def grade_task1(review_text: str, issues_found: list, severity: str) -> Dict:
    score = 0.0
    breakdown = {}
    review_lower = review_text.lower()
    issues_lower = [i.lower() for i in issues_found]
    all_text = review_lower + " ".join(issues_lower)

    # Check for off-by-one error detection (0.35 points)
    off_by_one_keywords = ["off-by-one", "off by one", "range", "index error", "indexerror", "len + 1"]
    if any(kw in all_text for kw in off_by_one_keywords):
        breakdown["off_by_one"] = 0.35
    else:
        breakdown["off_by_one"] = 0.0

    # Check for missing key/None check detection (0.35 points)
    none_keywords = ["key error", "keyerror", "none", "missing check", "missing key", "no check"]
    if any(kw in all_text for kw in none_keywords):
        breakdown["none_check"] = 0.35
    else:
        breakdown["none_check"] = 0.0

    # Severity match (0.30 points)
    if severity.lower() == "high":
        breakdown["severity"] = 0.30
    elif severity.lower() == "medium":
        breakdown["severity"] = 0.15
    else:
        breakdown["severity"] = 0.0

    score = sum(breakdown.values())
    score = round(min(score, 1.0), 2)

    return {
        "score": score,
        "breakdown": breakdown,
        "feedback": f"Task 1 score: {score}. Good job identifying bugs!" if score > 0.5 else f"Task 1 score: {score}. Try to identify more specific bugs."
    }


def grade_task2(review_text: str, issues_found: list, severity: str) -> Dict:
    score = 0.0
    breakdown = {}
    review_lower = review_text.lower()
    issues_lower = [i.lower() for i in issues_found]
    all_text = review_lower + " ".join(issues_lower)

    # SQL injection detection (0.30 points)
    sql_keywords = ["sql injection", "sql", "injection", "f-string", "format string", "unsafe query"]
    if any(kw in all_text for kw in sql_keywords):
        breakdown["sql_injection"] = 0.30
    else:
        breakdown["sql_injection"] = 0.0

    # Authentication check (0.25 points)
    auth_keywords = ["authentication", "auth", "no check", "missing check", "result check"]
    if any(kw in all_text for kw in auth_keywords):
        breakdown["auth_check"] = 0.25
    else:
        breakdown["auth_check"] = 0.0

    # Parameterized query suggestion (0.25 points)
    param_keywords = ["parameterized", "prepared statement", "placeholder", "?", "safe query"]
    if any(kw in all_text for kw in param_keywords):
        breakdown["parameterized"] = 0.25
    else:
        breakdown["parameterized"] = 0.0

    # Severity match (0.20 points)
    if severity.lower() == "high":
        breakdown["severity"] = 0.20
    elif severity.lower() == "medium":
        breakdown["severity"] = 0.10
    else:
        breakdown["severity"] = 0.0

    score = sum(breakdown.values())
    score = round(min(score, 1.0), 2)

    return {
        "score": score,
        "breakdown": breakdown,
        "feedback": f"Task 2 score: {score}. Security issues well identified!" if score > 0.5 else f"Task 2 score: {score}. Look deeper at security vulnerabilities."
    }


def grade_task3(review_text: str, issues_found: list, severity: str) -> Dict:
    score = 0.0
    breakdown = {}
    review_lower = review_text.lower()
    issues_lower = [i.lower() for i in issues_found]
    all_text = review_lower + " ".join(issues_lower)

    # Performance issue detection (0.20 points)
    perf_keywords = ["performance", "loop", "expensive", "optimize", "inefficient"]
    if any(kw in all_text for kw in perf_keywords):
        breakdown["performance"] = 0.20
    else:
        breakdown["performance"] = 0.0

    # Cache issue detection (0.20 points)
    cache_keywords = ["cache", "memory leak", "unbounded", "grows", "no limit", "size limit"]
    if any(kw in all_text for kw in cache_keywords):
        breakdown["cache"] = 0.20
    else:
        breakdown["cache"] = 0.0

    # Edge case detection (0.20 points)
    edge_keywords = ["edge case", "empty list", "empty", "none", "wrong type"]
    if any(kw in all_text for kw in edge_keywords):
        breakdown["edge_case"] = 0.20
    else:
        breakdown["edge_case"] = 0.0

    # Division error detection (0.20 points)
    div_keywords = ["division", "divide", "zero", "zerodivision", "zero check"]
    if any(kw in all_text for kw in div_keywords):
        breakdown["division"] = 0.20
    else:
        breakdown["division"] = 0.0

    # Severity match (0.20 points)
    if severity.lower() == "medium":
        breakdown["severity"] = 0.20
    elif severity.lower() == "high":
        breakdown["severity"] = 0.10
    else:
        breakdown["severity"] = 0.0

    score = sum(breakdown.values())
    score = round(min(score, 1.0), 2)

    return {
        "score": score,
        "breakdown": breakdown,
        "feedback": f"Task 3 score: {score}. Excellent refactor review!" if score > 0.5 else f"Task 3 score: {score}. This is a hard task — look for performance and edge case issues."
    }


GRADERS = {
    "task_1": grade_task1,
    "task_2": grade_task2,
    "task_3": grade_task3
}