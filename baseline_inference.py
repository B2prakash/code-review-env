import os
from openai import OpenAI
from env.environment import CodeReviewEnv, Action


def run_baseline():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    if not api_key:
        # Return mock scores if no API key available
        return {
            "task_1": {"score": 0.70, "status": "mock"},
            "task_2": {"score": 0.55, "status": "mock"},
            "task_3": {"score": 0.35, "status": "mock"},
            "note": "Set OPENAI_API_KEY environment variable for real scores"
        }

    client = OpenAI(api_key=api_key)
    env = CodeReviewEnv()
    results = {}

    for task_id in ["task_1", "task_2", "task_3"]:
        try:
            obs = env.reset(task_id)

            prompt = f"""You are an expert code reviewer.

Task: {obs.context}
Language: {obs.language}

Code to review:
{obs.code_diff}

Analyze the code and respond in this exact JSON format:
{{
    "review_text": "your detailed review here",
    "issues_found": ["issue1", "issue2", "issue3"],
    "severity": "low or medium or high"
}}

Be specific about bugs, security issues, and code quality problems."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            content = response.choices[0].message.content.strip()

            # Clean JSON response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            import json
            parsed = json.loads(content)

            action = Action(
                review_text=parsed.get("review_text", ""),
                issues_found=parsed.get("issues_found", []),
                severity=parsed.get("severity", "medium")
            )

            _, reward, _, _ = env.step(action)
            results[task_id] = {
                "score": reward.score,
                "breakdown": reward.breakdown,
                "feedback": reward.feedback,
                "status": "success"
            }

        except Exception as e:
            results[task_id] = {
                "score": 0.0,
                "status": "error",
                "error": str(e)
            }

    return results


if __name__ == "__main__":
    scores = run_baseline()
    for task_id, result in scores.items():
        print(f"{task_id}: {result}")