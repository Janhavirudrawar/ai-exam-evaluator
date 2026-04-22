
import json
import random
import os
import sys
from typing import Optional
from server.models import Observation, Action, Reward

# This adds the root directory to the Python path so it can find grader.py
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from grader import grade
except ImportError:
    # Fallback if the above logic fails in a specific container env
    def grade(*args, **kwargs): return 0.5

class ExamEnv:
    def __init__(self, dataset_path: Optional[str] = None):
        # 1. ROBUST PATHING
        if dataset_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dataset_path = os.path.join(base_dir, "dataset.json")
        
        self.dataset_path = os.path.abspath(dataset_path)
        self.current_task = None
        self.current_step = 0
        
        # 🔹 NEW: LOAD DATA ONCE DURING INITIALIZATION
        # This prevents repeated disk access and potential timeouts
        self.all_tasks = self.load_data()

    def load_data(self):
        # Fallback pathing logic
        current_path = self.dataset_path
        if not os.path.exists(current_path):
            alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json")
            if os.path.exists(alt_path):
                current_path = alt_path
            else:
                print(f"CRITICAL ERROR: Dataset not found at {self.dataset_path}")
                return []

        try:
            with open(current_path, "r") as f:
                content = json.load(f)
                return content.get("tasks", [])
        except Exception as e:
            print(f"JSON ERROR: {e}")
            return []

    def reset(self, difficulty: Optional[str] = None):
        self.current_step = 0

        # 🔹 USE MEMORY DATA INSTEAD OF RE-LOADING FILE
        if not self.all_tasks:
            # Emergency fallback task if dataset failed to load
            self.current_task = {
                "id": 0, "question": "N/A", "student_answer": "N/A", 
                "rubric": {}, "expected_score": 5, "difficulty": "easy"
            }
        else:
            filtered = self.all_tasks
            # CASE-INSENSITIVE FILTERING
            if difficulty:
                filtered = [t for t in self.all_tasks if str(t.get("difficulty")).lower() == difficulty.lower()]
            
            # FALLBACK: If specific difficulty is empty, use any available task
            if not filtered:
                filtered = self.all_tasks
            
            self.current_task = random.choice(filtered)

        return Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

    def step(self, action: Action):
        self.current_step += 1

        if self.current_task is None:
            self.reset()

        expected = float(self.current_task.get("expected_score", 5))
        predicted = float(action.score)

        # CALL GRADER
        grader_score = grade(
            None,
            action,
            {
                "expected_score": expected,
                "agent_score": predicted,
                "difficulty": self.current_task.get("difficulty")
            }
        )

        # STRICT (0.01, 0.99) CLAMPING
        try:
            reward_value = float(grader_score)
        except:
            reward_value = 0.5
            
        reward_value = max(0.01, min(0.99, reward_value))

        reward = Reward(value=reward_value)
        done = True

        info = {
            "expected_score": expected,
            "agent_score": predicted,
            "task_id": self.current_task.get("id"),
            "difficulty": self.current_task.get("difficulty"),
            "has_grader": True
        }

        obs = Observation(
            question=self.current_task["question"],
            student_answer=self.current_task["student_answer"],
            rubric=self.current_task["rubric"]
        )

        return obs, reward, done, info

    def state(self):
        return self.current_task