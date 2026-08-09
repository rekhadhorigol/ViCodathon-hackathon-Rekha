Links to chats with AI:
ChatGPT: (due to free tier, had to use multiple chats 😅)
1) https://chatgpt.com/share/6a7885a5-2938-83e8-8b39-20dd19f60542

2) https://chatgpt.com/share/6a7885cd-e000-83e8-b0f1-4b5474ead628

3) https://chatgpt.com/share/6a788618-212c-83ee-b4bf-dad4d48cf661

4) https://chatgpt.com/share/6a788d3e-94f8-83e8-a206-a8163a60744d


Claude:
https://claude.ai/share/85951813-0745-4c6b-8f80-fdec20f4b6b5


VS Git Copilot: used the prompts (mainly for frontend) given by chatgpt (can verify inside chatgpt links)


Important prompts of convo with AI:

# AI Usage Log

## Prompt 1

Project initialization.

Outcome:
Initialized repository and project structure.

## Prompt 2

### Prompt
Help me organize the project into a scalable React + FastAPI structure suitable for a hackathon while keeping the application runnable after each milestone.

### Outcome
- Organized backend into modular folders.
- Moved FastAPI entry point into `app/main.py`.
- Created frontend folder structure for future components.
- Generated `requirements.txt`.
- Ensured the backend continued running after restructuring.

## Prompt 3

### Prompt
Design a scalable backend architecture for an AI Interview Agent using FastAPI, separating API routes, business services, models, and data while keeping the codebase modular for future AI integration.

### Outcome
- Created modular backend folder structure.
- Separated API, services, models, and data layers.
- Prepared the project for implementing the interview endpoint.

## Prompt 4

### Prompt
Help me implement the first version of the interview API using FastAPI with proper request/response models and a service layer, returning a mock interview question while following a modular architecture.

### Outcome
- Implemented POST `/api/interview`.
- Added request and response models.
- Created the interview service.
- Connected API routes through FastAPI.
- Verified the endpoint using Swagger UI.

## Prompt 5

### Prompt
Implement reusable services to load the hackathon curriculum and candidate data from JSON files using pathlib, proper error handling, and type hints. Include a function to retrieve a candidate by their unique ID.

### Outcome
- Implemented curriculum loading service.
- Implemented candidate loading service.
- Added reusable JSON loading functions.
- Added candidate lookup functionality.
- Prepared backend for personalized interview generation.

## Prompt 6

### Prompt
Connect the interview API to the candidate service so it retrieves a candidate by ID from the provided JSON and returns the candidate details with proper error handling.

### Outcome
- Connected API with candidate service.
- Implemented candidate lookup.
- Added HTTP error handling.
- Verified candidate retrieval through Swagger.

## Prompt 7

### Prompt
Improve the curriculum service by validating the JSON structure and adding a helper function to retrieve curriculum details for a specific day.

### Outcome
- Added curriculum JSON validation.
- Added `get_day(day_number)` helper.
- Prepared curriculum lookup for dynamic interview question generation.

## Prompt 8

### Prompt
Implement the first version of the interview service that generates the opening interview question dynamically from the candidate's completed missions instead of using a hardcoded question.

### Outcome
- Built interview service.
- Selected completed missions dynamically.
- Generated personalized opening question.
- Connected the interview API to the interview service.

## Prompt 9

### Prompt
Implement an in-memory session service to maintain interview state. Store asked questions, answers, and the current interview progress for each session.

### Outcome
- Added session management.
- Stored interview progress.
- Prepared backend for multi-turn conversations.

## Prompt 10

### Prompt
Refactor the interview session management to use the provided sessionId instead of candidateId so multiple interview sessions can exist independently for the same candidate.

### Outcome
- Updated session management to use sessionId.
- Refactored interview service.
- Updated API integration.
- Aligned implementation with the hackathon API contract.

## Prompt 11

### Prompt
Extend the interview service to support multi-turn conversations by storing candidate answers in the interview session and incrementing the interview question number for each subsequent request.

### Outcome
- Added answer storage.
- Implemented multi-turn interview flow.
- Maintained interview state across requests.
- Prepared the backend for adaptive AI follow-up questions.

## Prompt 12

### Prompt
Integrate Gemini as the LLM for generating adaptive technical interview questions.

### Outcome
- Added Gemini API integration.
- Added secure environment-variable configuration.
- Added reusable Gemini service.
- Kept the API key outside the repository.

## Prompt 13

### Prompt
Build an adaptive technical interview engine using the candidate profile, completed missions, curriculum details, previous questions, and previous answers. Generate context-aware technical questions through Gemini while progressing across different completed curriculum topics.

### Outcome
- Added curriculum-aware question generation.
- Added candidate context to LLM prompts.
- Added previous interview context.
- Added adaptive follow-up question generation.
- Added progression across completed curriculum topics.
- Designed the flow to support the required 8-question, 4+ curriculum-day interview.


## Prompt 14

### Prompt

Extend the interview agent to evaluate each candidate answer against the current curriculum topic, learning objectives, candidate role, and years of experience. Store structured per-question evaluations and generate an overall assessment after all 8 questions are completed.

### Outcome

* Added structured per-question answer evaluation.
* Added technical accuracy, depth, clarity, relevance, and experience-aware assessment.
* Stored evaluations within the interview session.
* Added overall evaluation generation after interview completion.
* Added structured strengths, gaps, improvement areas, verdict, score, and recommendation.

## Prompt 15

### Prompt

Implement the technical-spec-compatible interview flow while preserving the existing frontend flow. Support the `/api/interview` contract with `sessionId`, `candidate`, and `message`, maintain multi-turn session state, return `reply` and `done`, and provide structured final feedback after completing the interview.

### Outcome

* Added a technical-spec-compatible interview flow.
* Preserved compatibility with the project's existing frontend.
* Added candidate resolution from the technical-spec candidate object.
* Maintained session state across multiple requests.
* Added `done` and structured `feedback` responses.
* Verified the complete 8-question interview lifecycle.

## Prompt 16

### Prompt

Add reliable Gemini API failure handling so transient AI failures are retried and persistent failures return a controlled HTTP 503 response instead of crashing the interview flow.

### Outcome

* Added Gemini retry handling.
* Added controlled `503 Service Unavailable` responses.
* Prevented individual AI service failures from producing uncontrolled backend errors.
* Kept the interview API predictable during temporary Gemini failures.

## Prompt 17

### Prompt

Review the complete AI Interview Agent against the hackathon requirements and verify the full lifecycle from candidate selection through adaptive questioning, per-question evaluation, interview completion, overall evaluation, and final results.

### Outcome

* Verified the complete interview lifecycle.
* Confirmed the minimum 8-question requirement.
* Verified multi-turn conversation state.
* Verified curriculum-aware question generation.
* Verified per-question evaluations.
* Verified overall evaluation generation.
* Tested the deployed frontend and backend integration.
* Confirmed the final interview result endpoint.

## Prompt 18

### Prompt

Prepare the AI Interview Agent for final hackathon submission by documenting the architecture, AI usage, technology stack, deployment, testing process, limitations, and future improvements while keeping the implementation aligned with the stated problem requirements.

### Outcome

* Documented the complete system architecture.
* Documented AI usage and prompt-driven development.
* Documented deployment and testing.
* Documented known prototype limitations.
* Documented future production improvements.
* Prepared the repository for final hackathon submission.

## Prompt 19

### Prompt

Improve the frontend API service reliability by adding retry handling for failed backend requests. The frontend should automatically retry a failed API request up to three times with a short delay between attempts, while displaying a controlled user-friendly error message if all attempts fail. Keep the existing interview API flow and mock API support unchanged.

### Outcome

* Added reusable retry logic for frontend API requests.
* Configured up to 3 attempts for failed requests.
* Added a 5-second delay between retry attempts.
* Preserved the existing interview and mock API flows.
* Added a controlled user-friendly error message when all retry attempts fail.
* Verified that the deployed 8-question interview flow continues to work successfully.

