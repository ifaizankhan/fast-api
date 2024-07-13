# FastAPI MCQ API

This FastAPI application serves multiple-choice questions (MCQs) based on specified criteria. Users can authenticate, retrieve questions, and add new questions (admin only).

## Setup

### Install Dependencies

1. Create a virtual environment:
    ```sh
    python3 -m venv env
    ```

2. Activate the virtual environment:
    ```sh
    source env/bin/activate  # On macOS/Linux
    .\env\Scripts\activate   # On Windows
    ```

3. Install required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Run the Server

Start the FastAPI server using Uvicorn:
```sh
uvicorn app:app --reload --port 8083

### Instructions for Testing

1. **Health Check**: Ensures the API is running.
    ```sh
    curl -X GET http://127.0.0.1:8083/api/health
    ```
2. **Authenticate User**: Verifies user credentials.
    ```sh
    curl -v -u alice:wonderland -X POST http://127.0.0.1:8083/api/auth
    ```
3. **Get Questions**: Retrieves a specified number of questions.
    ```sh
    curl -v -u alice:wonderland -X GET "http://127.0.0.1:8083/api/questions?use=Test%20de%20positionnement&subject=BDD&num_questions=2"
    ```
4. **Add a Question**: Allows an admin user to add a new question.
    ```sh
    curl -u admin:4dm1N -H "Content-Type: application/json" -X POST -d '{
        "question": "New question?",
        "subject": "BDD",
        "use": "Test de positionnement",
        "correct": "A",
        "responseA": "Answer A",
        "responseB": "Answer B",
        "responseC": "Answer C"
    }' http://127.0.0.1:8083/api/questions
    ```

This `README.md` provides clear instructions to set up, run, and test the FastAPI application, ensuring it meets the specified requirements, including the health check command.