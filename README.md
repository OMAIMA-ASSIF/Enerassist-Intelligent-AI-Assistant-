# AI Chatbot Backend

A production-ready AI chatbot backend built with FastAPI, LangChain, and Qdrant.

## Prerequisites

- Python 3.11+
- MongoDB Atlas Account
- Qdrant Cloud Account
- Mistral AI API Key

## Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd CHATBOT_H15
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**
    
    You need to create two `.env` files based on the examples provided.

    *   **Server Config**: Copy `server/.env.example` to `server/.env` and fill in your MongoDB URI and Secret Key.
        ```bash
        cp server/.env.example server/.env
        ```
    
    *   **AI Config**: Copy `ai/.env.example` to `ai/.env` and fill in your Qdrant and Mistral API keys.
        ```bash
        cp ai/.env.example ai/.env
        ```

    **Note:** The `.env` files contain sensitive keys and are ignored by git. You must create them locally for the project to function.

5.  **Run the Server**
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

## API Usage Example

### 1. Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```
*Copy the `access_token` from the response.*

### 3. Send Message
```bash
curl -X POST http://localhost:8000/chat/send \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?"
  }'
```

## Project Structure
- `server/`: Core FastAPI backend, auth, and database routes.
- `ai/`: LangChain logic, Qdrant integration, and chatbot implementation.
- `main.py`: Entry point for the application. 
