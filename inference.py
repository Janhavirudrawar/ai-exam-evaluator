
# import asyncio
# import os
# from typing import List, Optional
# from dotenv import load_dotenv
# load_dotenv()


# from openai import OpenAI

# # 🔹 Your environment
# from server.environment import ExamEnv
# from server.models import Action

# # ==============================
# # CONFIGURATION
# # ==============================


# # API_KEY = os.getenv("HF_TOKEN")
# API_KEY = os.getenv("OPENAI_API_KEY")
# # API_BASE_URL = os.getenv("API_BASE_URL") or "https://api-inference.huggingface.co/models"
# API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
# MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
# # IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# TASK_NAME = "exam-evaluator"
# BENCHMARK = "exam_env"
# MAX_STEPS = 2
# SUCCESS_SCORE_THRESHOLD = 0.1
# MAX_SCORE_PER_STEP = 10.0  # max marks per step

# # ==============================
# # SYSTEM PROMPT
# # ==============================
# SYSTEM_PROMPT = """
# You are an AI exam evaluator.

# You will be given:
# - Question
# - Student Answer
# - Rubric (total marks = 10)

# Your task:
# - Assign a score between 1 and 10

# Rules:
# - Follow rubric strictly
# - Be fair and consistent
# - Return ONLY a number (no explanation)
# """

# # ==============================
# # LOGGING FUNCTIONS
# # ==============================
# def log_start(task: str, env: str, model: str):
#     print(f"[START] task={task} env={env} model={model}", flush=True)

# def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
#     error_val = error if error else "null"
#     print(
#         f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
#         flush=True
#     )

# def log_end(success: bool, steps: int, score: float, rewards: List[float]):
#     rewards_str = ",".join(f"{r:.2f}" for r in rewards)
#     print(
#         f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
#         flush=True
#     )


# def build_prompt(obs, step, history):
#     return f"""
# You are an exam evaluator improving your score step by step.

# Step: {step}/5

# Question:
# {obs['question']}

# Student Answer:
# {obs['student_answer']}

# Rubric:
# {obs['rubric']}

# Previous Attempts:
# {history}

# Instructions:
# - Try to improve your score each step
# - Learn from previous attempts
# - Give ONLY a number between 0 to 10

# Output format:
# {{"score": <number>}}
# """
# def fallback_score(obs):
#     # simple input-based fallback (no manual constant)
#     words = len(obs.student_answer.split())

#     if words < 20:
#         return 3
#     elif words < 50:
#         return 5
#     else:
#         return 7


# def get_score(client, obs, step, history):
#     prompt = f"""
# Question: {obs.question}
# Student Answer: {obs.student_answer}
# Rubric: {obs.rubric}

# Give a score between 0 and 10.
# Only return a number.
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}],
#             timeout=15   
#         )

#         import re
#         match = re.search(r"\d+", response.choices[0].message.content)

#         if match:
#             return int(match.group())
#         else:
#             return fallback_score(obs)

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return fallback_score(obs)

# def main():
#     client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
#     # Docker image or local env
#     env = ExamEnv()  # Just create the environment normally

#     rewards: List[float] = []
#     steps_taken = 0
#     score = 0.0
#     success = False

#     log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

#     try:
#         # obs = env.reset()
#         obs = env.reset()
#         if isinstance(obs, tuple):
#            obs = obs[0]

        
        
#         history = []  # 🔥 NEW

#         for step in range(1, MAX_STEPS + 1):

#     # 🔥 UPDATED: pass step + history
#           score_pred = get_score(client, obs, step, history)

#           action = Action(score=score_pred)

#           obs, reward, done, info = env.step(action)

#     # 🔹 handle reward object
#           if hasattr(reward, "value"):
#             reward = reward.value
#           elif hasattr(reward, "score"):
#             reward = reward.score
#           else:
#             reward = float(reward) if reward is not None else 0.0

#           error = None

#           rewards.append(reward)
#           steps_taken = step

#     # 🔥 ADD history
#           history.append(f"Step {step}: score={score_pred}, reward={reward}")

#           log_step(step, str(int(score_pred)), reward, done, error)

#           if done:
#             break

#         # max_total = MAX_STEPS * MAX_SCORE_PER_STEP
#         # score = sum(rewards) / max_total if max_total > 0 else 0.0
#         score = sum(rewards) / len(rewards) if rewards else 0.0
#         score = min(max(score, 0.0), 1.0)
#         success = score >= SUCCESS_SCORE_THRESHOLD

#     finally:
#         try:
#             pass
#         except Exception as e:
#             print(f"[DEBUG] close error: {e}", flush=True)
#         log_end(success, steps_taken, score, rewards)

# if __name__ == "__main__":
#     main()

# import os
# from typing import List, Optional
# from dotenv import load_dotenv

# load_dotenv()

# from openai import OpenAI

# from server.environment import ExamEnv
# from server.models import Action

# # ==============================
# # CONFIG
# # ==============================

# API_KEY = os.getenv("API_KEY")
# API_BASE_URL = os.getenv("API_BASE_URL" , "https://router.huggingface.co/v1")
# # API_KEY = os.environ["API_KEY"]
# # API_BASE_URL = os.environ["API_BASE_URL"]

# # API_KEY = os.environ.get("API_KEY", "dummy_key")
# # API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")

# MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

# TASK_NAME = "exam-evaluator"
# BENCHMARK = "exam_env"
# MAX_STEPS = 2
# SUCCESS_SCORE_THRESHOLD = 0.1

# # ==============================
# # LOGGING
# # ==============================

# def log_start(task: str, env: str, model: str):
#     print(f"[START] task={task} env={env} model={model}", flush=True)

# def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
#     error_val = error if error else "null"
#     print(
#         f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
#         flush=True
#     )

# def log_end(success: bool, steps: int, score: float, rewards: List[float]):
#     rewards_str = ",".join(f"{r:.2f}" for r in rewards)
#     print(
#         f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
#         flush=True
#     )

# # ==============================
# # FALLBACK (IMPORTANT)
# # ==============================

# def fallback_score(obs):
#     words = len(obs.student_answer.split())

#     if words < 10:
#         return 2
#     elif words < 30:
#         return 4
#     elif words < 60:
#         return 6
#     else:
#         return 8

# # ==============================
# # MODEL CALL (SAFE)
# # ==============================

# def get_score(client, obs, step, history):
#     # 🔥 If no client → fallback immediately
#     # if client is None:
#     #     return fallback_score(obs)

#     prompt = f"""
# Question: {obs.question}
# Student Answer: {obs.student_answer}
# Rubric: {obs.rubric}

# Give a score between 0 and 10.
# Only return a number.
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}],
#             timeout=15
#         )

#         import re
#         match = re.search(r"\d+", response.choices[0].message.content)

#         if match:
#             return int(match.group())
#         else:
#             return fallback_score(obs)

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return fallback_score(obs)

# # ==============================
# # MAIN
# # ==============================

# # def main():
  
# #     client = None
# #     if API_KEY:
# #         try:
# #             client  = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
# #         except Exception as e:
# #             print("Client init failed:", e)
# #             client = None

# #     client = OpenAI(
# #     base_url=API_BASE_URL,
# #     api_key=API_KEY
# #      )
# #     env = ExamEnv()


# #     client = OpenAI(
# #     base_url=API_BASE_URL,
# #     api_key=API_KEY
# # )

# # 🔥🔥 ADD THIS BLOCK HERE (VERY IMPORTANT)


# def main():
#     print("🚀 MAIN STARTED")

#     # ✅ Create client ONLY ONCE
#     client = None
#     if API_KEY:
#         try:
#             client = OpenAI(
#                 base_url=API_BASE_URL,
#                 api_key=API_KEY
#             )
#             print("Client created")
#         except Exception as e:
#             print("Client init failed:", e)

#     # ✅ Warmup call
#     if client:
#         try:
#             response = client.chat.completions.create(
#                 model=MODEL_NAME,
#                 messages=[{"role": "user", "content": "hello"}]
#             )
#             print("Warmup OK")
#         except Exception as e:
#             print("Warmup failed:", e)

#     # ✅ Create environment
#     env = ExamEnv()

#     rewards: List[float] = []
#     steps_taken = 0
#     score = 0.0
#     success = False

#     log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

#     try:
#         obs = env.reset()
#         if isinstance(obs, tuple):
#             obs = obs[0]

#         history = []

#         for step in range(1, MAX_STEPS + 1):

#             score_pred = get_score(client, obs, step, history)
#             action = Action(score=score_pred)

#             obs, reward, done, info = env.step(action)

#             if hasattr(reward, "value"):
#                 reward = reward.value
#             elif hasattr(reward, "score"):
#                 reward = reward.score
#             else:
#                 reward = float(reward) if reward is not None else 0.0

#             rewards.append(reward)
#             steps_taken = step

#             history.append(f"Step {step}: score={score_pred}, reward={reward}")

#             log_step(step, str(int(score_pred)), reward, done, None)

#             if done:
#                 break

#         score = sum(rewards) / len(rewards) if rewards else 0.0
#         score = min(max(score, 0.0), 1.0)
#         success = score >= SUCCESS_SCORE_THRESHOLD

#     except Exception as e:
#         print("FATAL ERROR:", e)

#     finally:
#         log_end(success, steps_taken, score, rewards)
# # try:
#     # response = client.chat.completions.create(
#     #     model=MODEL_NAME,
#     #     messages=[{"role": "user", "content": "hello"}]
# #     # )
# #     print("Warmup OK")
# # except Exception as e:
# #     print("Warmup failed:", e)

# # Continue your code
#     env = ExamEnv()

#     rewards: List[float] = []
#     steps_taken = 0
#     score = 0.0
#     success = False

#     log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

#     try:
#         obs = env.reset()
#         if isinstance(obs, tuple):
#             obs = obs[0]

#         history = []

#         for step in range(1, MAX_STEPS + 1):

#             score_pred = get_score(client, obs, step, history)
#             action = Action(score=score_pred)

#             obs, reward, done, info = env.step(action)

#             # Normalize reward
#             if hasattr(reward, "value"):
#                 reward = reward.value
#             elif hasattr(reward, "score"):
#                 reward = reward.score
#             else:
#                 reward = float(reward) if reward is not None else 0.0

#             rewards.append(reward)
#             steps_taken = step

#             history.append(f"Step {step}: score={score_pred}, reward={reward}")

#             log_step(step, str(int(score_pred)), reward, done, None)

#             if done:
#                 break

#         score = sum(rewards) / len(rewards) if rewards else 0.0
#         score = min(max(score, 0.0), 1.0)
#         success = score >= SUCCESS_SCORE_THRESHOLD

#     except Exception as e:
#         print("FATAL ERROR:", e)

#     finally:
#         log_end(success, steps_taken, score, rewards)

#         # ==============================

# if __name__ == "__main__":
#     main()

# # ==============================

import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from server.environment import ExamEnv
from server.models import Action

# ==============================
# CONFIG (IMPORTANT)
# ==============================

API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

TASK_NAME = "exam-evaluator"
BENCHMARK = "exam_env"

MAX_STEPS = 2
SUCCESS_SCORE_THRESHOLD = 0.1

# ==============================
# LOGGING (DO NOT CHANGE)
# ==============================

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


# ==============================
# FALLBACK (ONLY FOR FAILURE)
# ==============================

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

# ==============================
# LLM CALL (MANDATORY)
# ==============================

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

# ==============================
# MAIN
# ==============================

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

# import os
# from typing import List, Optional
# from dotenv import load_dotenv

# load_dotenv()

# from openai import OpenAI
# from server.environment import ExamEnv
# from server.models import Action

# # ==============================
# # CONFIG
# # ==============================

# API_KEY = os.environ["API_KEY"]
# API_BASE_URL = os.environ["API_BASE_URL"]
# MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

# TASK_NAME = "exam-evaluator"
# BENCHMARK = "exam_env"

# MAX_STEPS = 1   # 🔥 keep it 1 for speed
# SUCCESS_SCORE_THRESHOLD = 0.1

# # ==============================
# # LOGGING (STRICT FORMAT)
# # ==============================

# def log_start(task: str, env: str, model: str):
#     print(f"[START] task={task} env={env} model={model}", flush=True)

# def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
#     error_val = error if error else "null"
#     print(
#         f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
#         flush=True
#     )

# def log_end(success: bool, steps: int, score: float, rewards: List[float]):
#     rewards_str = ",".join(f"{r:.2f}" for r in rewards)
#     print(
#         f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
#         flush=True
#     )

# # ==============================
# # LLM CALL
# # ==============================

# def get_score(client, obs):
#     prompt = f"""
# Question: {obs.question}
# Student Answer: {obs.student_answer}
# Rubric: {obs.rubric}

# Give a score between 0 and 10.
# Only return a number.
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}],
#             timeout=15
#         )

#         import re
#         match = re.search(r"\d+", response.choices[0].message.content)

#         if match:
#             return int(match.group())
#         return 5  # fallback neutral

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return 5  # fallback

# # ==============================
# # MAIN
# # ==============================

# def main():
#     client = OpenAI(
#         base_url=API_BASE_URL,
#         api_key=API_KEY
#     )

#     env = ExamEnv()

#     rewards: List[float] = []
#     steps_taken = 0
#     success = False

#     log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

#     try:
#         # 🔥 RUN ALL 3 TASKS
#         for difficulty in ["easy", "medium", "hard"]:

#             obs = env.reset(difficulty=difficulty)

#             for step in range(1, MAX_STEPS + 1):

#                 score_pred = get_score(client, obs)
#                 action = Action(score=score_pred)

#                 obs, reward, done, info = env.step(action)

#                 # normalize reward
#                 if hasattr(reward, "value"):
#                     reward = reward.value
#                 else:
#                     reward = float(reward)

#                 rewards.append(reward)
#                 steps_taken += 1

#                 log_step(step, str(score_pred), reward, done, None)

#                 if done:
#                     break

#         # final scoring
#         score = sum(rewards) / len(rewards) if rewards else 0.0
#         score = min(max(score, 0.0), 1.0)
#         success = score >= SUCCESS_SCORE_THRESHOLD

#     except Exception as e:
#         print("FATAL ERROR:", e)

#     finally:
#         log_end(success, steps_taken, score, rewards)


# if __name__ == "__main__":
#     main()
# import os
# import re
# from typing import List, Optional
# from dotenv import load_dotenv

# load_dotenv()

# from openai import OpenAI
# from server.environment import ExamEnv
# from server.models import Action

# # ==============================
# # CONFIG
# # ==============================

# # Use .get() to prevent KeyErrors if variables are missing
# API_KEY = os.environ.get("API_KEY")
# API_BASE_URL = os.environ.get("API_BASE_URL")
# MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

# BENCHMARK = "exam_env"
# MAX_STEPS = 1   # keep it fast
# SUCCESS_SCORE_THRESHOLD = 0.1

# # 3 DISTINCT TASKS AS REQUIRED
# TASKS = [
#     ("exam-evaluator-easy", "easy"),
#     ("exam-evaluator-medium", "medium"),
#     ("exam-evaluator-hard", "hard"),
# ]

# # ==============================
# # LOGGING (STRICT FORMAT)
# # ==============================

# def log_start(task: str, env: str, model: str):
#     print(f"[START] task={task} env={env} model={model}", flush=True)

# def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
#     error_val = error if error else "null"
#     print(
#         f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
#         flush=True
#     )

# def log_end(success: bool, steps: int, score: float, rewards: List[float]):
#     rewards_str = ",".join(f"{r:.2f}" for r in rewards)
#     print(
#         f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
#         flush=True
#     )

# # ==============================
# # LLM CALL
# # ==============================

# def get_score(client, obs):
#     prompt = f"""
# Question: {obs.question}
# Student Answer: {obs.student_answer}
# Rubric: {obs.rubric}

# Give a score between 0 and 10.
# Only return the number.
# """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}],
#             timeout=15
#         )

#         content = response.choices[0].message.content
#         match = re.search(r"\d+", content)

#         if match:
#             return int(match.group())

#         return 5  # fallback

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return 5  # fallback


# # ==============================
# # MAIN
# # ==============================

# def main():
#     if not API_KEY:
#         print("FATAL ERROR: API_KEY missing from environment.")
#         return

#     client = OpenAI(
#         base_url=API_BASE_URL,
#         api_key=API_KEY
#     )

#     env = ExamEnv()

#     try:
#         for task_name, difficulty in TASKS:
#             rewards: List[float] = []
#             steps_taken = 0

#             log_start(task_name, BENCHMARK, MODEL_NAME)

#             # reset() uses the new filtering logic in environment.py
#             obs = env.reset(difficulty=difficulty)

#             for step in range(1, MAX_STEPS + 1):
#                 score_pred = get_score(client, obs)
                
#                 # Create the action object
#                 action = Action(score=score_pred)

#                 obs, reward_obj, done, info = env.step(action)

#                 # Robust extraction of the reward value
#                 try:
#                     curr_reward = float(getattr(reward_obj, "value", reward_obj))
#                 except (TypeError, ValueError):
#                     curr_reward = 0.5

#                 # DOUBLE-CLAMP: Ensure execution log reward is strictly (0,1)
#                 curr_reward = max(0.01, min(0.99, curr_reward))

#                 rewards.append(curr_reward)
#                 steps_taken += 1

#                 log_step(step, str(score_pred), curr_reward, done, None)

#                 if done:
#                     break

#             # Calculate the final task average
#             score = sum(rewards) / len(rewards) if rewards else 0.5
            
#             # FINAL CLAMP: Must stay inside 0.01 to 0.99 for the log
#             final_clamped_score = float(max(0.01, min(0.99, score)))
#             success = final_clamped_score >= SUCCESS_SCORE_THRESHOLD

#             log_end(success, steps_taken, final_clamped_score, rewards)

#     except Exception as e:
#         print("FATAL SYSTEM ERROR:", e)


# if __name__ == "__main__":
#     main()