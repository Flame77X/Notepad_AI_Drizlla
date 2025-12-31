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

## 3. System Workflows

Here is how each component works within the system:

### 🖥️ Frontend (React + Vite)
*   **Role**: User Interface & State Management.
*   **Workflow**:
    1.  User interacts with the UI (Login, Dashboard, Chat).
    2.  `App.jsx` checks for a valid Supabase Session.
    3.  Requests are sent to the **FastAPI Backend**, including the User's Access Token.

### 🧠 Backend (FastAPI + Python)
*   **Role**: Logic Core, AI Processing, & Security.
*   **Workflow**:
    1.  Receives request (e.g., `/chat` message).
    2.  **`auth.py`** validates the Supabase Token.
    3.  Fetches context (Notes/Events) from Supabase.
    4.  Constructs a prompt and sends it to the **AI Engine**.
    5.  Parses the AI response for **Actions** (Create Note/Event).

### 🤖 AI Engine (Pollinations.ai)
*   **Role**: Natural Language Understanding.
*   **Workflow**:
    1.  Receives the prompt with context.
    2.  Generates a text response.
    3.  If the user asked to "Schedule a meeting", it outputs a structured command like `[ACTION:EVENT|...]`.

### 🗄️ Database (Supabase)
*   **Role**: Auth, Data Storage & RLS.
*   **Workflow**:
    1.  **Auth**: Handles User Sign Up/Login -> Returns JWT.
    2.  **Data**: Stores Notes/Events.
    3.  **RLS**: Enforces that `user_id` matches the requester.

### 🕒 Time Parsing (dateparser)
*   **Role**: Converting "Human Time" to "Computer Time".
*   **Workflow**:
    1.  Input: *"Next Friday at 2pm"*
    2.  Processing: `dateparser` calculates the exact ISO timestamp based on the current date.
    3.  Output: `2025-01-10T14:00:00` (ready for database).

---

## 4. Directory Structure & Key Files

### 🟢 Backend (`notepad-backend/`)
*   **`main.py` (The Brain)**: Handles endpoints(`/chat`, `/notes`), AI calls, and Action Parsing.
*   **`auth.py` (Security)**: Validates User Tokens.
*   **`.env` (Secrets)**: Stores API Keys (`SUPABASE_URL`, `SUPABASE_KEY`).

### 🔵 Frontend (`notepad-frontend/src/`)
*   **`App.jsx` (The Interface)**: Main React component for Dashboard, Login, and Chat.
*   **`.env.local`**: Stores Frontend Keys (`VITE_SUPABASE_URL`).

---

## 5. Development Challenges & Solutions

### 🔴 Error: "AI Endpoint Not Available (410 Gone)"
*   **Problem**: Hugging Face free API was deprecating generic inference endpoints.
*   **Solution**: Switched to **Pollinations.ai**, which provides stable, free text generation via GET requests.

### 🔴 Error: "AI Can't Schedule Events"
*   **Problem**: The AI didn't know how to convert relative dates like "next Friday" into a specific timestamp.
*   **Solution**: Integrated **`dateparser`** in the backend to parse relative time strings into ISO format.

### 🔴 Security Vulnerability
*   **Problem**: API keys were initially hardcoded in the source files.
*   **Solution**: Moved all keys to `.env` files and performed a codebase audit to ensure no secrets remained.

---

## 6. Security & Deployment

*   **Row Level Security (RLS)**: Enabled on Supabase. Users can strictly only see rows matching their own `user_id`.
*   **Environment Variables**: All API keys are git-ignored and not present in the repository.

---

## 🤖 7. AI Command Guide

The AI Assistant is designed to be an **active agent**. Here is how to control it:

### 📝 Create a Note
**Command:** *"Create a note: [Title] - [Content]"*
> **Example:** *"Create a note: Project Ideas - Use React and Python for the hackathon."*

### 📅 Schedule an Event
**Command:** *"Schedule [Event] [Time]"*
> **Example:** *"Schedule a meeting with the team next Friday at 2 PM."*
> **Example:** *"Remind me to call John tomorrow morning."*

### 🧠 Ask Contextual Questions
**Command:** Ask anything about your stored data.
> **Example:** *"Do I have any events this week?"*

---

## ⚙️ 8. Setup & Deployment Guide

### Option A: Running Locally (For Development)

**1. Backend Setup**
```bash
cd notepad-backend
python -m venv venv
# Activate: .\venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt

# Create .env file with:
# SUPABASE_URL=...
# SUPABASE_KEY=...

uvicorn main:app --reload
```

**2. Frontend Setup**
```bash
cd notepad-frontend
npm install

# Create .env.local file with:
# VITE_SUPABASE_URL=...
# VITE_SUPABASE_ANON_KEY=...

npm run dev
```

### Option B: Hosting (For Production)

To host this project online (e.g., on **Render**, **Vercel**, or **Heroku**), follow these simplified steps:

**1. Database (Supabase)**
*   Your Supabase project is already in the cloud. You do not need to redeploy it.

**2. Backend Hosting (e.g., Render Web Service)**
*   Connect your GitHub repo.
*   Set Build Command: `pip install -r requirements.txt`
*   Set Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
*   **Crucial:** Add `SUPABASE_URL` and `SUPABASE_KEY` to the service's Environment Variables.

**3. Frontend Hosting (e.g., Vercel)**
*   Connect your GitHub repo to Vercel.
*   **Crucial:** Add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` to Vercel's Environment Variables.
*   Once deployed, update your Backend CORS settings to allow requests from your new Frontend URL.

---

**Developed by Flame77X**