# # grader.py

# def grade(question: str, student_answer: str, rubric: str) -> float:
#     """
#     Grades a student's answer based on a simple heuristic.

#     Args:
#         question (str): The question asked
#         student_answer (str): The student's response
#         rubric (str): Expected answer / guideline

#     Returns:
#         float: Score between 0.0 and 1.0
#     """

#     # Safety checks
#     if not student_answer or not rubric:
#         return 0.0

#     # Normalize text
#     student_answer = student_answer.lower().strip()
#     rubric = rubric.lower().strip()

#     # Tokenize
#     student_words = set(student_answer.split())
#     rubric_words = set(rubric.split())

#     if not rubric_words:
#         return 0.0

#     # Calculate overlap score
#     common_words = student_words.intersection(rubric_words)
#     score = len(common_words) / len(rubric_words)

#     # Clamp score between 0 and 1
#     score = max(0.0, min(1.0, score))

#     return score
# def grade(observation, action, info):
#     """
#     Calculates the reward based on the difference between expected and predicted scores.
#     Ensures the output is strictly within the (0.01, 0.99) range.
#     """
#     try:
#         # Ensure we are working with floats to avoid type errors
#         expected = float(info.get("expected_score", 0))
#         predicted = float(info.get("agent_score", 0))

#         # Calculate absolute difference
#         diff = abs(predicted - expected)

#         # Base score calculation (Normalized to 1.0)
#         # Assuming the max possible score in your dataset is 10.0
#         score = 1.0 - (diff / 10.0)

#         # 🔥 Clamp STRICTLY between 0.01 and 0.99
#         # This prevents the 'Out of Range' error from the validator
#         if score <= 0.0:
#             score = 0.01
#         elif score >= 1.0:
#             score = 0.99
#         else:
#             score = float(score)

#         return score

#     except Exception as e:
#         # Fallback reward so the validator doesn't crash if info is missing
#         print(f"Grader Error: {e}")
#         return 0.5

# Grader.py
# grader.py
from typing import Dict, Any

class Grader:
    def __init__(self, task_id: str):
        self.task_id = task_id

    def grade(self, observation: Dict[str, Any], action: Dict[str, Any]) -> float:
        try:
            # Note: your environment.py passes 'expected_score' in the context_dict
            # We use .get() to check both 'rubric_score' and 'expected_score'
            true_score = float(observation.get("expected_score", observation.get("rubric_score", 0)))
            
            # Action is passed as an object or dict; we handle both
            if hasattr(action, "score"):
                pred_score = float(action.score)
            else:
                pred_score = float(action.get("score", 0))

            diff = abs(true_score - pred_score) / 10.0
            reward = max(0.0, 1.0 - diff)

            print(
                f"[GRADER] task={self.task_id} | true={true_score:.2f} "
                f"| pred={pred_score:.2f} | reward={reward:.3f}",
                flush=True
            )
            return reward
        except Exception as e:
            print(f"[GRADER] Error: {e}", flush=True)
            return 0.0

# 🔹 ADD THIS FUNCTION AT THE BOTTOM
# This matches the call: grade(None, action, context_dict)
def grade(obs_placeholder, action, context):
    # Extract task_id from context if available
    t_id = context.get("task_id", "unknown")
    g = Grader(task_id=t_id)
    # We pass the 'context' as the observation because it contains the true score
    return g.grade(context, action)