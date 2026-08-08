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