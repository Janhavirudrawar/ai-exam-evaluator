

import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from server.environment import ExamEnv
from server.models import Action


# CONFIG 


API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

TASK_NAME = "exam-evaluator"
BENCHMARK = "exam_env"

MAX_STEPS = 2
SUCCESS_SCORE_THRESHOLD = 0.1


# LOGGING 


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True
    )



# FALLBACK 


def fallback_score(obs):
    words = len(obs.student_answer.split())

    if words < 10:
        return 2
    elif words < 30:
        return 4
    elif words < 60:
        return 6
    else:
        return 8


# LLM CALL 


def get_score(client, obs):
    prompt = f"""
Question: {obs.question}
Student Answer: {obs.student_answer}
Rubric: {obs.rubric}

Give a score between 0 and 10.
Only return a number.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            timeout=15   
        )

        import re
        match = re.search(r"\d+", response.choices[0].message.content)

        if match:
            return int(match.group())
        else:
            return fallback_score(obs)

    except Exception as e:
        print("LLM ERROR:", e)
        return fallback_score(obs)


# MAIN


def main():
   
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )

    env = ExamEnv()

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        obs = env.reset()
        if isinstance(obs, tuple):
            obs = obs[0]

        for step in range(1, MAX_STEPS + 1):

            
            score_pred = get_score(client, obs)

            action = Action(score=score_pred)

            obs, reward, done, info = env.step(action)

            # Normalize reward
            if hasattr(reward, "value"):
                reward = reward.value
            elif hasattr(reward, "score"):
                reward = reward.score
            else:
                reward = float(reward) if reward is not None else 0.0

            rewards.append(reward)
            steps_taken = step

            log_step(step, str(int(score_pred)), reward, done, None)

            if done:
                break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print("FATAL ERROR:", e)

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    main()

