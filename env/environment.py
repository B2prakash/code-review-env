from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from env.tasks import TASKS
from env.graders import GRADERS


class Observation(BaseModel):
    task_id: str
    code_diff: str
    language: str
    context: str
    turn: int


class Action(BaseModel):
    review_text: str
    issues_found: List[str]
    severity: str


class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float]
    feedback: str


class CodeReviewEnv:
    def __init__(self):
        self.current_task_id = None
        self.current_task = None
        self.turn = 0
        self.max_turns = 5
        self.done = False
        self.last_reward = None
        self.history = []

    def reset(self, task_id: str = "task_1") -> Observation:
        if task_id not in TASKS:
            task_id = "task_1"

        self.current_task_id = task_id
        self.current_task = TASKS[task_id]
        self.turn = 0
        self.max_turns = self.current_task["max_turns"]
        self.done = False
        self.last_reward = None
        self.history = []

        return Observation(
            task_id=task_id,
            code_diff=self.current_task["code_diff"],
            language=self.current_task["language"],
            context=self.current_task["description"],
            turn=self.turn
        )

    def step(self, action: Action):
        if self.done:
            obs = Observation(
                task_id=self.current_task_id,
                code_diff=self.current_task["code_diff"],
                language=self.current_task["language"],
                context=self.current_task["description"],
                turn=self.turn
            )
            return obs, self.last_reward, True, {"message": "Episode already done"}

        self.turn += 1

        # Run grader
        grader_fn = GRADERS[self.current_task_id]
        result = grader_fn(
            review_text=action.review_text,
            issues_found=action.issues_found,
            severity=action.severity
        )

        # Shape the reward
        score = result["score"]

        # Penalty for very short reviews
        if len(action.review_text) < 50:
            score = max(0.0, score - 0.1)
            result["feedback"] += " Review too short."

        # Penalty for empty issues
        if len(action.issues_found) == 0:
            score = max(0.0, score - 0.1)
            result["feedback"] += " No issues listed."

        score = round(min(score, 1.0), 2)
        result["score"] = score

        reward = Reward(
            score=score,
            breakdown=result["breakdown"],
            feedback=result["feedback"]
        )

        self.last_reward = reward
        self.history.append({
            "turn": self.turn,
            "action": action.dict(),
            "reward": reward.dict()
        })

        # Check if done
        if self.turn >= self.max_turns or score >= 0.9:
            self.done = True

        obs = Observation(
            task_id=self.current_task_id,
            code_diff=self.current_task["code_diff"],
            language=self.current_task["language"],
            context=self.current_task["description"],
            turn=self.turn
        )

        return obs, reward, self.done, {"turn": self.turn}

    def state(self) -> Dict[str, Any]:
        return {
            "current_task_id": self.current_task_id,
            "turn": self.turn,
            "max_turns": self.max_turns,
            "done": self.done,
            "last_reward": self.last_reward.dict() if self.last_reward else None,
            "history": self.history
        }

    def get_last_grade(self) -> Dict[str, Any]:
        if self.last_reward:
            return self.last_reward.dict()
        return {"score": 0.0, "breakdown": {}, "feedback": "No action taken yet"}