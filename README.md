# Properties Dashboard

**A productivity application that combines personal notes, event scheduling, and an Agentic AI Assistant.**

---

## 1. Project Overview

**Properties Dashboard** is a productivity application designed to streamline your workflow. It features an **Agentic AI Assistant** capable of context-aware interactions and executing actions on your behalf.

### Core Philosophy
*   **Context Awareness**: The AI reads your notes and calendar to provide relevant answers.
*   **Agency**: The AI can act on your behalf, such as creating notes or scheduling events via natural language commands.
*   **Security**: Enterprise-grade data isolation using **Supabase Row Level Security (RLS)**.

---

## 2. Technology Stack

| Component | Choice | Why we used it |
| :--- | :--- | :--- |
| **Frontend** | **React (Vite)** | Fast development server and industry-standard component model. |
| **Backend** | **FastAPI (Python)** | High performance, easy integration with AI libraries. |
| **Database** | **Supabase (PostgreSQL)** | Handles authentication and data storage with Row Level Security. |
| **AI Engine** | **Pollinations.ai** | **Cost-Effective Solution**. We use this free API to power the chat assistant, avoiding the credit limits/costs of OpenAI or Hugging Face. |
| **Time Parsing** | **dateparser** | Python library used to convert natural language time (e.g., "tomorrow at 5") into database timestamps. |

---

## 3. Directory Structure & Key Files

### 🟢 Backend (`notepad-backend/`)
*   **`main.py` (The Brain)**
    *   **AI Integration**: Uses `requests.get()` to call Pollinations.ai.
    *   **Agent Logic**: Contains a custom parser that intercepts AI responses starting with `[ACTION:NOTE|...]` or `[ACTION:EVENT|...]` to execute database inserts automatically.
    *   **Endpoints**: `/chat`, `/notes`, `/events`.
*   **`auth.py` (Security)**
    *   Validates Supabase JWTs (JSON Web Tokens) to ensure requests are authorized.
*   **`.env` (Secrets)**
    *   Stores `SUPABASE_URL` and `SUPABASE_KEY` securely.

### 🔵 Frontend (`notepad-frontend/src/`)
*   **`App.jsx` (The Interface)**
    *   **State**: Manages notes, events, and session (Auth).
    *   **UI Features**:
        *   **Login/Signup Toggle**: Users can register or log in.
        *   **Dashboard**: Displays notes in a grid.
        *   **Status Updates**: Dropdown to mark notes as Pending, In Progress, or Done.
        *   **AI Chat**: A chat interface that sends user queries + context to the FastAPI backend.
*   **`.env.local`**
    *   Stores `VITE_SUPABASE_URL` and `VITE_SUPABASE_KEY`.

---

## 4. Development Challenges & Solutions

### 🔴 Error: "AI Endpoint Not Available (410 Gone)"
*   **Problem**: The Hugging Face free API we initially tried (Phi-3.5) was deprecated or rate-limited.
*   **Solution**: Switched to **Pollinations.ai**, which provides stable, free text generation via GET requests.

### 🔴 Error: "AI Can't Schedule Events"
*   **Problem**: The AI didn't know how to convert relative dates like "next Friday" into a specific timestamp.
*   **Solution**: Integrated **`dateparser`** in the backend to parse relative time strings into ISO format.

### 🔴 Security Vulnerability
*   **Problem**: API keys were initially hardcoded in the source files.
*   **Solution**: Moved all keys to `.env` files and performed a codebase audit to ensure no secrets remained.

---

## 5. Security & Deployment

*   **Row Level Security (RLS)**: Enabled on Supabase. Users can strictly only see rows matching their own `user_id`.
*   **Environment Variables**: All API keys are git-ignored and not present in the repository.

---

## ⚙️ Setup Instructions

### 1. Backend Setup
```bash
cd notepad-backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd notepad-frontend
npm install
npm run dev
```