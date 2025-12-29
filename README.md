# 🌿 Sage Protocol (Formerly Notepad AI)

**A secure, AI-powered productivity dashboard built for the modern era.**

> **Status**: Active Development  
> **Version**: 1.0.0 (Sage Protocol Upgrade)

---

## 🚀 Overview

**Sage Protocol** is more than just a notepad. It's an intelligent workspace that combines secure note-taking with an Agentic AI assistant capable of performing real actions.

Built with a **Security-First** mindset, the application ensures all credentials are managed via environment variables and offers a robust User Registration system powered by Supabase.

### ✨ Key Features

*   **🤖 Agentic AI Assistant**:
    *   **Chat with Llama 3.2**: integrated via Pollinations.ai / Hugging Face.
    *   **AI Actions**: The AI can **Create Notes** and **Schedule Events** for you.
        *   *"Remind me to buy milk tomorrow at 10 AM"* -> **Creates Event**
        *   *"Save a note about the meeting"* -> **Creates Note**
    *   **Natural Language Processing**: Uses `dateparser` to understand complex time commands.

*   **🔒 Enterprise-Grade Security**:
    *   **No Hardcoded Secrets**: All API keys and credentials are strictly managed via `.env` files.
    *   **Supabase Authentication**: Secure Sign Up & Login flow with email verification.
    *   **Row Level Security (RLS)**: Users can only see their own data.

*   **🎨 "Sage" UI Design**:
    *   Custom CSS system (`SageStyles`) for a focused, brutalist-inspired aesthetic.
    *   Responsive Dashboard with Note filtering and Calendar views.

---

## 🛠️ Tech Stack

### **Frontend**
*   **React (Vite)**: Fast, modern UI framework.
*   **Lucide React**: Beautiful, consistent iconography.
*   **Supabase-JS**: Client-side authentication and database subscription.

### **Backend**
*   **FastAPI (Python)**: High-performance backend API.
*   **Uvicorn**: ASGI server.
*   **Dateparser**: For parsing natural language dates/times.
*   **Pollinations.ai / Hugging Face**: LLM Inference Providers.

### **Database & Auth**
*   **Supabase (PostgreSQL)**: Scalable relational database with built-in Auth and RLS.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Flame77X/Notepad_AI_Drizlla.git
cd Notepad_AI_Drizlla
```

### 2. Backend Setup
Navigate to the `notepad-backend` directory and set up the Python environment.

```bash
cd notepad-backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**Configuration (.env)**  
Create a `.env` file in `notepad-backend/` with:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
# Optional: Hugging Face Token if using HF Inference directly
HF_TOKEN=your_hf_token
```

**Run Server**:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
Navigate to the `notepad-frontend` directory.

```bash
cd ../notepad-frontend
npm install
```

**Configuration (.env.local)**  
Create a `.env.local` file in `notepad-frontend/` with:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Run Client**:
```bash
npm run dev
```

---

## 🖼️ Usage

1.  **Register/Login**: Create an account via the Sign-Up toggle.
2.  **Dashboard**: View your notes and upcoming events.
3.  **Chat**: Open the AI Assistant sidebar.
    *   Try: *"Create a note: Project Ideas - Use React and Python"*
    *   Try: *"Schedule a meeting for next Friday at 2pm"*

---

## 🛡️ Security Audit

*   **Secret Scanning**: Repository has been audited for leaked keys.
*   **Git History**: Clean history with no sensitive data.
*   **Access Control**: Backend verifies JWT tokens on every protected endpoint.

---

**Developed by Flame77X**