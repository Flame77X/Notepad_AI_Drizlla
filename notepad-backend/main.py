"""
Properties Dashboard - FastAPI Backend with AI Integration
Supabase + Hugging Face Microsoft Phi-3.5-mini-instruct AI Chat
"""

from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from database import supabase
from auth import get_current_user
import requests

# ===== AI CONFIGURATION =====
# Using Pollinations.ai (Free, reliable, no token needed)
POLLINATIONS_API_URL = "https://text.pollinations.ai/"

# ===== FASTAPI SETUP =====
app = FastAPI(
    title="Properties Dashboard API with AI",
    version="1.0.0",
    description="Supabase + Pollinations.ai Backend"
)

# ===== CORS MIDDLEWARE =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Pydantic Models
# -----------------------

class NoteStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class NoteCreate(BaseModel):
    title: str
    content: str
    status: NoteStatus = NoteStatus.PENDING

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[NoteStatus] = None

# -----------------------
# Health Check Endpoints
# -----------------------

@app.get("/")
def root():
    """API health check"""
    return {
        "status": "Backend running successfully",
        "service": "Properties Dashboard API with AI",
        "version": "1.0.0",
        "ai_model": "Phi-3.5-mini-instruct (Microsoft via Hugging Face)"
    }

@app.get("/health")
def health_check():
    """Simple health check for monitoring"""
    return {"status": "ok"}

# =============================================
# NOTES ENDPOINTS (CRUD with Supabase)
# =============================================

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, user: dict = Depends(get_current_user)):
    """Create a new note for authenticated user"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = supabase.table("notes").insert({
            "title": note.title,
            "content": note.content,
            "status": note.status.value,
            "user_id": user_id,
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create note")
        
        return response.data[0] if response.data else {"message": "Created"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/notes")
def get_notes(user: dict = Depends(get_current_user)):
    """Get all notes for authenticated user"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = (
            supabase.table("notes")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data if response.data else []
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/notes/{note_id}")
def update_note(note_id: str, note: NoteUpdate, user: dict = Depends(get_current_user)):
    """Update a note"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    update_data = note.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    try:
        response = (
            supabase.table("notes")
            .update(update_data)
            .eq("id", note_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Note not found or unauthorized")
        
        return response.data[0] if response.data else {"message": "Updated"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/notes/{note_id}")
def delete_note(note_id: str, user: dict = Depends(get_current_user)):
    """Delete a note"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = (
            supabase.table("notes")
            .delete()
            .eq("id", note_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Note not found or unauthorized")
        
        return {"message": "Note deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# =============================================
# EVENTS ENDPOINTS (CRUD with Supabase)
# =============================================

@app.post("/events", status_code=201)
def create_event(
    title: str = Form(...),
    description: str = Form(default=""),
    start_time: str = Form(...),
    end_time: str = Form(...),
    user: dict = Depends(get_current_user)
):
    """Create a new event for authenticated user"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = supabase.table("events").insert({
            "title": title,
            "description": description,
            "start_time": start_time,
            "end_time": end_time,
            "user_id": user_id,
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create event")
        
        return response.data[0] if response.data else {"message": "Created"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/events")
def get_events(user: dict = Depends(get_current_user)):
    """Get all events for authenticated user, ordered by start time"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = (
            supabase.table("events")
            .select("*")
            .eq("user_id", user_id)
            .order("start_time", desc=False)
            .execute()
        )
        return response.data if response.data else []
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/events/{event_id}")
def delete_event(event_id: str, user: dict = Depends(get_current_user)):
    """Delete an event"""
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    try:
        response = (
            supabase.table("events")
            .delete()
            .eq("id", event_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Event not found or unauthorized")
        
        return {"message": "Event deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ========================================
# 🤖 AI CHAT ENDPOINT (NEW!)
# ========================================

@app.post("/chat")
def chat(
    message: str = Form(...),
    user: dict = Depends(get_current_user)
):
    """
    AI Chat endpoint using Phi-3.5-mini-instruct via Hugging Face
    Considers user's notes and events as context
    """
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1️⃣ FETCH USER CONTEXT (from Supabase)
    try:
        notes_response = (
            supabase.table("notes")
            .select("title,content")
            .eq("user_id", user_id)
            .execute()
        )
        notes = notes_response.data or []

        events_response = (
            supabase.table("events")
            .select("title,start_time")
            .eq("user_id", user_id)
            .execute()
        )
        events = events_response.data or []
    except Exception as e:
        print(f"[DEBUG] Error fetching context: {str(e)}")
        notes = []
        events = []

    # 2️⃣ BUILD CONTEXT STRING
    context_str = ""
    if notes:
        context_str += "User Notes:\n"
        for note in notes[:3]:  # Limit to 3 notes
            note_title = note.get("title", "Untitled")
            note_content = note.get("content", "")
            context_str += f"- {note_title}: {note_content}\n"
    
    if events:
        context_str += "\nUpcoming Events:\n"
        for event in events[:3]:  # Limit to 3 events
            event_title = event.get("title", "Untitled")
            event_time = event.get("start_time", "Unknown time")
            context_str += f"- {event_title} at {event_time}\n"

    # 3️⃣ BUILD PROMPT
    # Minimal prompt to keep URL length safe
    # We add instructions for ACTIONS
    system_instruction = (
        "System: You are a helpful assistant. "
        "To create a note, start reply with: [ACTION:NOTE|Title|Content]. "
        "To create an event, start reply with: [ACTION:EVENT|Title|Time Description]. "
        "Otherwise, just reply normally."
    )
    
    full_prompt = f"{system_instruction}\nContext:\n{context_str}\nUser: {message}\nAssistant:"
    
    # 4️⃣ CALL POLLINATIONS.AI (GET REQUEST)
    import urllib.parse
    import dateparser # pip install dateparser
    
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"{POLLINATIONS_API_URL}{encoded_prompt}"

    try:
        print(f"[DEBUG] Calling Pollinations: {url[:50]}...") # Log partial URL
        response = requests.get(url, timeout=30)

        print(f"[DEBUG] Response status: {response.status_code}")

        if response.status_code != 200:
             return {"reply": f"⚠️ AI Error ({response.status_code}). Please try again."}

        # 5️⃣ EXTRACT RESPONSE AND CHECK FOR ACTIONS
        reply_text = response.text.strip()

        
        # --- ACTION HANDLER ---
        if reply_text.startswith("[ACTION:"):
            try:
                # Expected format: [ACTION:NOTE|Title|Content]
                # Remove brackets
                clean_cmd = reply_text[1:-1] # ACTION:NOTE|Title|Content
                parts = clean_cmd.split("|")
                
                action_type = parts[0].split(":")[1] # NOTE or EVENT
                
                if action_type == "NOTE" and len(parts) >= 3:
                     title = parts[1]
                     content = parts[2]
                     supabase.table("notes").insert({
                        "title": title,
                        "content": content,
                        "status": "Pending",
                        "user_id": user["id"]
                     }).execute()
                     return {"reply": f"✅ I've created the note: '{title}'."}
                     
                elif action_type == "EVENT" and len(parts) >= 3:
                     title = parts[1]
                     time_str = parts[2]
                     
                     # Magic time parsing
                     dt = dateparser.parse(time_str)
                     
                     if dt:
                         # Default duration 1 hour
                         from datetime import timedelta
                         end_dt = dt + timedelta(hours=1)
                         
                         supabase.table("events").insert({
                            "title": title,
                            "description": f"Scheduled via AI: {time_str}",
                            "start_time": dt.isoformat(),
                            "end_time": end_dt.isoformat(),
                            "user_id": user["id"]
                         }).execute()
                         return {"reply": f"✅ Scheduled '{title}' for {dt.strftime('%b %d at %I:%M %p')}."}
                     else:
                         return {"reply": f"⚠️ I understood you wanted an event, but I couldn't understand the time '{time_str}'."}
                         
            except Exception as e:
                print(f"[DEBUG] Action failed: {e}")
                return {"reply": "⚠️ I tried to perform that action but something went wrong."}
        
        # --- END ACTION HANDLER ---

        return {"reply": reply_text}

    except requests.exceptions.Timeout:
        return {"reply": "⏱️ AI request timed out. Please try again."}
    
    except Exception as e:
        print(f"[DEBUG] Chat error: {str(e)}")
        return {"reply": f"❌ Error: {str(e)}"}


# -----------------------
# RUN SERVER
# -----------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
