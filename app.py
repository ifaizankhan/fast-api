from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import random
import secrets

app = FastAPI()

# Load the dataset
questions_df = pd.read_excel('questions_en.xlsx')

# User credentials
users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, credentials.username)
    correct_password = secrets.compare_digest(credentials.password, users.get(credentials.username, ""))
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username

@app.get("/api/health")
async def health_check():
    return {"status": "API is up and running!"}

@app.post("/api/auth")
async def auth_user(username: str = Depends(authenticate)):
    return {"message": "Authentication successful."}

@app.get("/api/questions")
async def get_questions(
    use: Optional[str] = None,
    subject: Optional[str] = None,
    num_questions: int = 5,
    username: str = Depends(authenticate)
):
    filtered_questions = questions_df
    if use:
        filtered_questions = filtered_questions[filtered_questions['use'] == use]
    if subject:
        filtered_questions = filtered_questions[filtered_questions['subject'] == subject]

    available_count = len(filtered_questions)
    print(f"Filtered Questions Count: {available_count}")
    print(filtered_questions)

    if num_questions > available_count:
        return {
            "message": f"Not enough questions available. Only {available_count} questions available.",
            "available_questions": filtered_questions.fillna("").to_dict(orient='records')
        }

    questions_list = filtered_questions.sample(n=num_questions).fillna("").to_dict(orient='records')
    return questions_list

class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None

@app.post("/api/questions")
async def add_question(
    question: Question,
    username: str = Depends(authenticate)
):
    if username != "admin":
        raise HTTPException(status_code=403, detail="Admin authentication required")

    new_question = pd.DataFrame([question.dict()])
    global questions_df
    questions_df = pd.concat([questions_df, new_question], ignore_index=True)
    questions_df.to_excel('questions_en.xlsx', index=False)
    return {"message": "Question added successfully."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8083)