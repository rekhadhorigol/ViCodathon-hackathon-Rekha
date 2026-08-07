from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="AI Interview Agent")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Backend is running!"}