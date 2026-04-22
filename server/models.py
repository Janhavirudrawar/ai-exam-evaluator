from pydantic import BaseModel
from typing import Dict

class Observation(BaseModel):
    question: str
    student_answer: str
    rubric: Dict[str, int]

class Action(BaseModel):
    score: float
    

class Reward(BaseModel):
    value: float
   
