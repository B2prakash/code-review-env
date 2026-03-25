# Code Review Environment

An OpenEnv environment for training AI agents to review code diffs.

## Description
This environment simulates real-world code review tasks where an AI agent
must identify bugs, security vulnerabilities, and code quality issues.

## Tasks
- **Task 1 (Easy)**: Bug Identification — find off-by-one and missing checks
- **Task 2 (Medium)**: Security Audit — find SQL injection and auth issues  
- **Task 3 (Hard)**: Refactor Quality Review — find performance and edge case bugs

## Action Space
```json
{
  "review_text": "your detailed review",
  "issues_found": ["issue1", "issue2"],
  "severity": "low | medium | high"
}
```

## Observation Space
```json
{
  "task_id": "task_1",
  "code_diff": "code to review",
  "language": "python",
  "context": "task description",
  "turn": 0
}
```

## Setup
```bash
pip install fastapi uvicorn pydantic openai
uvicorn api.main:app --host 0.0.0.0 --port 7860
```

## Docker
```bash
docker build -t code-review-env .
docker run -p 7860:7860 code-review-env
```

## Baseline
```bash
export OPENAI_API_KEY=your_key_here
python baseline_inference.py
```

## Endpoints
- `POST /reset` — Start a new episode
- `POST /step` — Take an action
- `GET /state` — Get current state
- `GET /tasks` — List all tasks
- `POST /grader` — Get last grade
- `POST /baseline` — Run baseline agent

## Author
B2prakash