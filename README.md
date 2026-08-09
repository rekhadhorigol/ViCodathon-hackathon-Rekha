# Intmate — Your AI Interview Agent
By Rekha Dhorigol

> **ViCodathon Hackathon — Problem Statement 2: The Interview Agent**
> **Build the interviewer, not the interview.**

**Intmate** is an AI-powered technical interview platform that conducts personalized, multi-turn interviews based on a candidate's learning journey through the 31-day AI Cohort.

---

## 🚀 At a Glance

**Intmate** transforms curriculum progress into an adaptive technical interview:

**Completed Learning → Candidate Context → AI Question → Candidate Answer → Evaluation → Adaptive Follow-up → Final Assessment**

The platform conducts a minimum 8-question interview and produces both per-question evaluations and a final technical assessment.

---

## 🎯 Problem

The AI Cohort is a 31-day enterprise AI engineering program covering topics such as:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Prompt Engineering
* Agentic AI
* Model Context Protocol (MCP)
* AI Deployment
* Production AI Systems

Although learners complete practical AI engineering work throughout the cohort, preparing for technical interviews and explaining their engineering decisions remains challenging.

Traditional interview systems often rely on fixed question sets and do not account for what a candidate has actually learned.

**Intmate solves this by generating a personalized technical interview from the candidate's completed learning journey.**

---

## 💡 Solution

Intmate conducts an adaptive, multi-turn technical interview that:

1. Identifies the candidate's completed curriculum topics.
2. Generates technical questions grounded in those topics.
3. Uses previous questions and answers as conversation context.
4. Adapts subsequent questions based on the candidate's responses.
5. Evaluates each answer for technical quality.
6. Produces a structured overall assessment at the end.

The goal is to make the interaction feel like a **real technical interview rather than a scripted questionnaire**.

---

## 🌟 Why Intmate?

Intmate is useful because it turns a candidate's actual learning progress into a realistic technical interview.

Instead of asking every candidate the same predefined questions, it:

- Tests what the candidate has actually learned.
- Adjusts question difficulty based on responses.
- Connects questions to the candidate's completed curriculum.
- Evaluates both individual answers and overall technical performance.
- Provides actionable strengths, gaps, and improvement recommendations.

This makes the interview more personalized, context-aware, and useful for identifying real technical readiness.

---

## ✨ Key Features

### Personalized Interviews

Questions are generated from the candidate's completed curriculum missions rather than from a generic question bank.

### Adaptive Questioning

The agent considers the candidate's latest answer:

* Weak or incomplete answer → focused follow-up
* Strong answer → increased difficulty or practical scenario
* Previous answers → maintained as interview context

### Multi-Turn Context

The interview maintains:

* Previous questions
* Candidate answers
* Assessed curriculum topics
* Question-topic associations

This allows the AI interviewer to maintain continuity throughout the interview.

### Experience-Aware Assessment

Questions and evaluations consider the candidate's recorded role and years of experience.

Candidate experience is taken from the provided candidate profile rather than being entered manually during setup.

### Per-Question Evaluation

Each answer is evaluated on:

* Technical accuracy
* Depth of understanding
* Clarity
* Relevance
* Experience appropriateness

### Overall Assessment

After the interview, Intmate generates:

* Overall score
* Verdict
* Technical strengths
* Technical gaps
* Strongest areas
* Areas for improvement
* Recommendation

### Gemini Failure Handling

The Gemini service includes a retry mechanism.

If Gemini fails twice, the backend returns a controlled `503 Service Unavailable` response instead of allowing the request to fail unpredictably.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Candidate Profile │
                    │   + Curriculum Data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │       Vercel        │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │       Render        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
       │ Interview    │ │ Evaluation  │ │   Session    │
       │ Service      │ │ Services    │ │   Service    │
       └──────┬───────┘ └──────┬──────┘ └──────────────┘
              │                │
              └────────┬───────┘
                       ▼
              ┌──────────────────┐
              │    Gemini API    │
              │  AI Generation   │
              └──────────────────┘
```

---

## 🔄 Interview Flow

```text
Candidate selected
        │
        ▼
Load candidate profile
        │
        ▼
Identify completed curriculum missions
        │
        ▼
Generate technical question
        │
        ▼
Candidate answers
        │
        ▼
Evaluate answer
        │
        ▼
Use previous Q&A as context
        │
        ▼
Generate adaptive next question
        │
        ▼
Repeat until 8 questions
        │
        ▼
Generate overall evaluation
        │
        ▼
Display interview results
```

---

## 📋 Hackathon Requirements

The implementation is designed around the requirements of **ViCodathon Problem Statement 2 — The Interview Agent**.

| Requirement                        | Implementation                                                                   |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| Conversational technical interview | Multi-turn React + FastAPI interview flow                                        |
| Minimum 8 questions                | Interview limit configured to 8 questions                                        |
| At least 4 curriculum days         | Questions are grounded in completed curriculum missions and rotate across topics |
| Follow-up questions                | Gemini receives the latest answer and previous interview context                 |
| Conversation context               | Previous questions and answers are included in generation context                |
| Structured feedback                | Per-question and overall evaluations are generated as structured JSON            |
| Required HTTP API                  | FastAPI exposes interview and evaluation endpoints                               |

---

## 🧠 AI Interviewer

Intmate uses Gemini for three major AI tasks.

### 1. Question Generation

The model receives:

* Candidate role
* Candidate experience
* Current curriculum topic
* Learning objectives
* Tools
* Previous interview questions and answers
* Latest candidate answer

It is instructed to:

* Probe weaknesses with follow-ups
* Increase difficulty after strong answers
* Avoid repeating questions
* Prefer practical engineering scenarios
* Match candidate experience
* Stay within completed curriculum topics
* Generate exactly one technical question

### 2. Answer Evaluation

Each answer is evaluated against:

* Technical accuracy
* Depth
* Clarity
* Relevance
* Candidate experience level

The result is returned as structured JSON.

### 3. Overall Evaluation

After the interview, Gemini synthesizes the individual evaluations into an overall assessment containing the candidate's strengths, gaps, improvement areas, verdict, score, and recommendation.

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* React Router
* Vercel

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* Render

### AI

- Google Gemini API
- Gemini Flash Lite
- Prompt-based adaptive question generation
- LLM-based answer evaluation
- LLM-based overall assessment

### Data

* JSON-based curriculum
* JSON-based synthetic candidate profiles
* In-memory interview session storage

---

## 📁 Project Structure

```text
ViCodathon/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── data/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── candidate_service.py
│   │   │   ├── curriculum_service.py
│   │   │   ├── evaluation_service.py
│   │   │   ├── gemini_service.py
│   │   │   ├── interview_service.py
│   │   │   ├── overall_evaluation_service.py
│   │   │   └── session_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── data/
│   │   ├── pages/
│   │   ├── components/
│   │   └── utils/
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Running Locally

### Prerequisites

* Python 3.10+
* Node.js
* npm
* A Gemini API key

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ViCodathon
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

### 3. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will provide the local frontend URL.

Configure the frontend API base URL:

```env
VITE_API_BASE=http://localhost:8000
```

---

## 🔐 Environment Variables

### Backend

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend

```env
VITE_API_BASE=http://localhost:8000
VITE_USE_MOCK_AI=false
```

**Never commit real API keys to Git.**

The deployed backend receives the Gemini API key through the hosting provider's environment-variable configuration.

---

## 🌐 Live Demo

### Frontend

https://ai-interview-agent-vicodathon.vercel.app/

### Backend

https://ai-interview-agent-vicodathon.onrender.com/

---

## 🧪 Testing

The final testing process verifies the complete interview lifecycle:

```text
Setup
  ↓
Start Interview
  ↓
Question 1
  ↓
Answer
  ↓
Evaluation
  ↓
Adaptive Question
  ↓
...
  ↓
Question 8
  ↓
Complete Interview
  ↓
Overall Evaluation
  ↓
Results
```

Testing verifies:

* Complete 8-question interview flow
* Gemini API communication
* Adaptive question generation
* Per-question evaluation
* Overall evaluation
* API communication
* CORS configuration
* Deployment
* Candidate experience data
* Structured evaluation responses
* Gemini failure handling

---

## 🛡️ Reliability

Gemini generation uses a retry mechanism.

If the first Gemini request fails, the service attempts the request once more.

If both attempts fail, the backend returns:

```text
503 Service Unavailable
AI service is temporarily unavailable. Please try again.
```

This prevents an individual AI service failure from producing an uncontrolled backend error.

---

## ⚡ Demo & Deployment Notes

The backend is deployed on Render's Free tier. Free Render web services automatically spin down after a period of inactivity and require a short cold-start period when the next request arrives.

Because of this, the **first interaction with the backend after inactivity may take longer than subsequent requests**. During a live demonstration, it is recommended to open the application and allow the backend a short time to wake up before beginning the interview.

The interview itself is fully functional, but AI-powered operations naturally take a few seconds because each question generation and answer evaluation requires a Gemini API request. In particular:

* The first question may take slightly longer if the backend is waking from inactivity.
* After submitting an answer, generating and evaluating the next question may take a few seconds.
* After the eighth question, generating the final overall evaluation may take additional time because the system synthesizes the complete interview history and individual evaluations.

These delays are expected for an AI-powered prototype and are primarily caused by **LLM inference latency and the Render Free-tier cold start**, rather than frontend processing.


## 📌 Scope & Limitations

This implementation follows the hackathon scope and uses synthetic challenge data.

Current prototype limitations include:

* Interview sessions use in-memory storage.
* Candidate and curriculum data are provided as JSON.
* Authentication is not implemented.
* Long-term conversation history is not implemented.
* Voice interaction is not implemented.
* The application is designed primarily as a hackathon prototype.

These limitations are intentional and appropriate for the current hackathon prototype scope.

---

## 🔮 Future Improvements

Potential production extensions include:

* Persistent database-backed interview sessions
* Authentication and candidate accounts
* Richer candidate-learning analytics
* More sophisticated curriculum-topic tracking
* Voice-based interviews
* Interview difficulty calibration across sessions
* Human interviewer review
* Analytics dashboards
* Advanced agent orchestration
* Production-grade observability and monitoring

---

## 🏆 Hackathon Context

**Hackathon:** ViCodathon
**Problem Statement:** 2 — The Interview Agent

The challenge asks participants to **build the interviewer, not the interview**: an AI agent capable of conducting a realistic, personalized, multi-turn technical interview based on a candidate's learning journey.

Intmate addresses this by connecting:

**Curriculum Progress → Candidate Context → Adaptive Questioning → Answer Evaluation → Final Assessment**

into one complete interview experience.

---

## 👤 Participant

**Participant:** Rekha Dhorigol

**Participation:** Solo

**Project:** Intmate — Your AI Interview Agent

---

## 📄 License

This project was developed as a hackathon submission using the synthetic curriculum and candidate data provided for the challenge.

*Author: Rekha Dhorigol*