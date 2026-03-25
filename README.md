---
title: Code Review Env
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

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
- review_text: your detailed review
- issues_found: list of issues
- severity: low, medium or high

## Observation Space
- task_id, code_diff, language, context, turn

## Setup
pip install fastapi uvicorn pydantic openai
uvicorn api.main:app --host 0.0.0.0 --port 7860

## Docker
docker build -t code-review-env .
docker run -p 7860:7860 code-review-env

## Baseline
export OPENAI_API_KEY=your_key_here
python baseline_inference.py

## Endpoints
- POST /reset — Start a new episode
- POST /step — Take an action
- GET /state — Get current state
- GET /tasks — List all tasks
- POST /grader — Get last grade
- POST /baseline — Run baseline agent

## Author
B2prakash