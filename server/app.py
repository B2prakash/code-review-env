from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from env.environment import CodeReviewEnv, Action

app = FastAPI(
    title="Code Review Environment",
    description="An OpenEnv environment for training AI agents to review code",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

env = CodeReviewEnv()


@app.get("/")
def root():
    return {
        "name": "code-review-env",
        "version": "1.0.0",
        "description": "OpenEnv environment for AI code review agents",
        "endpoints": ["/reset", "/step", "/state", "/tasks", "/grader", "/baseline"]
    }


@app.post("/reset")
def reset(task_id: str = "task_1"):
    obs = env.reset(task_id)
    return obs.dict()


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()


@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {"id": "task_1", "name": "Bug Identification", "difficulty": "easy", "max_turns": 5},
            {"id": "task_2", "name": "Security Audit", "difficulty": "medium", "max_turns": 5},
            {"id": "task_3", "name": "Refactor Quality Review", "difficulty": "hard", "max_turns": 8}
        ],
        "action_schema": Action.schema()
    }


@app.post("/grader")
def grader():
    return env.get_last_grade()


@app.post("/baseline")
def baseline():
    try:
        from inference import run_baseline
        results = run_baseline()
        return results
    except Exception as e:
        return {"error": str(e)}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()