
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