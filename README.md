
---
title: AI Exam Evaluator
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: Dockerfile
pinned: true
---

# AI Exam Evaluator (LLM + OpenEnv)

An AI-powered grading system that evaluates student answers using Large Language Models and a custom reinforcement learning-style environment built with OpenEnv.

---

## Overview

This project simulates automated evaluation of subjective exam answers using structured rubrics and reward-based scoring.

It is designed to mimic real-world educational grading systems used in ed-tech platforms.

---

##  Features

- Multi-task evaluation (easy, medium, hard)
- Custom reward-based grading system
- LLM-based scoring using API integration
- Fallback scoring for reliability
- Fast inference with timeout handling
- Docker-based deployment
- OpenEnv-compliant environment

---

##  How It Works

1. Environment loads a question, student answer, and rubric  
2. LLM predicts a score for the answer  
3. Environment compares predicted score with expected score  
4. Reward is calculated based on accuracy  
5. Results are logged in structured format  

---

## Environment Design

### Observation Space

```json
{
  "question": "Exam question",
  "student_answer": "Student response",
  "rubric": "Evaluation criteria"
}
Action Space
{
  "score": 0-10
}
Reward Function

Reward is based on how close the predicted score is to the expected score:

reward = max(0, 1 - abs(predicted - expected) / 10)

Includes:

Accuracy-based reward
Progress-based bonus/penalty
🧪 Tasks
Easy → factual questions
Medium → reasoning-based answers
Hard → analytical responses
🔗 API Endpoints
POST /reset → start new task
POST /step → submit score
GET /state → get current state
🛠️ Tech Stack
Python
FastAPI
OpenAI / Hugging Face API
Docker
OpenEnv
⚙️ Setup
Run with Docker
docker build -t exam-env .
docker run -p 7860:7860 exam-env
Run locally
pip install -r requirements.txt
uvicorn server.app:app --reload
🤖 Inference
python inference.py

Example output:

[START] task=exam-evaluator ...
[STEP] ...
[END] success=true score=0.65
📁 Project Structure
server/
 ├── app.py
 ├── environment.py
 ├── models.py
 ├── grader.py
 ├── inference.py
 ├── dataset.json

openenv.yaml
Dockerfile
requirements.txt
README.md
☁️ Deployment

Deployed using Docker on Hugging Face Spaces.

📌 Notes

This project demonstrates:

LLM integration in evaluation systems
Reinforcement learning environment design
Scalable grading automation
🤝 Development

Developed as part of a small team and later extended with additional improvements.
The project focuses on building an AI-driven evaluation system using LLMs and a custom OpenEnv-based environment.

📄 License

MIT License


---

