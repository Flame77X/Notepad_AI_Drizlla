import React, { useState, useEffect } from "react";
import {
  Trash2,
  LogOut,
  RefreshCw,
  Square,
  Layers,
  Clock,
  MessageSquare,
  Sparkles,
  ChevronRight,
} from "lucide-react";


const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_KEY;
const API_BASE = "http://127.0.0.1:8000";


// --- LLM helper ---
async function askAssistant(message, token) {
  const formData = new FormData();
  formData.append("message", message);

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Chat request failed: ${res.status} ${text}`);
  }
  const data = await res.json();
  return data.reply;
}


export default function App() {
  const [supabaseClient, setSupabaseClient] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Notes
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // Events
  const [events, setEvents] = useState([]);
  const [eventTitle, setEventTitle] = useState("");
  const [eventDesc, setEventDesc] = useState("");
  const [eventStart, setEventStart] = useState("");
  const [eventEnd, setEventEnd] = useState("");

  // Auth form
  const [email, setEmail] = useState(""); // Cleared default
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false); // Toggle state

  // AI assistant
  const [aiQuestion, setAiQuestion] = useState("");
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  // load Supabase SDK and session
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2";
    script.async = true;
    script.onload = () => {
      if (window.supabase) {
        const client = window.supabase.createClient(
          SUPABASE_URL,
          SUPABASE_KEY
        );
        setSupabaseClient(client);
        client.auth.getSession().then(({ data }) => setSession(data.session));
        client.auth.onAuthStateChange((_e, s) => setSession(s));
      }
    };
    document.body.appendChild(script);
    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  useEffect(() => {
    if (session) {
      fetchNotes();
      fetchEvents();
    }
  }, [session]);

  const fetchNotes = async () => {
    if (!session) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/notes`, {
        headers: { Authorization: `Bearer ${session.access_token}` },
      });
      if (res.ok) setNotes(await res.json());
      else setError("Failed to load notes");
    } catch (_err) {
      setError("Backend Sync Error");
    } finally {
      setLoading(false);
    }
  };

  const fetchEvents = async () => {
    if (!session) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/events`, {
        headers: { Authorization: `Bearer ${session.access_token}` },
      });
      if (res.ok) setEvents(await res.json());
    } catch (_err) {
      setError("Schedule Sync Error");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!supabaseClient) return;
    setLoading(true);
    setError("");
    const { data, error: authErr } =
      await supabaseClient.auth.signInWithPassword({ email, password });
    if (authErr) setError(authErr.message);
    setLoading(false);
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    if (!supabaseClient) return;
    setLoading(true);
    setError("");
    const { data, error: authErr } =
      await supabaseClient.auth.signUp({ email, password });
    if (authErr) {
      setError(authErr.message);
    } else {
      if (data.session) {
        setSession(data.session);
      } else {
        setError("Account created! Please check your email to confirm.");
      }
    }
    setLoading(false);
  };

  // ✅ FIXED: Use JSON instead of FormData
  const createNote = async (e) => {
    e.preventDefault();
    if (!session || !title.trim() || !content.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/notes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({
          title: title,
          content: content,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to create note");
      }

      setTitle("");
      setContent("");
      fetchNotes();
    } catch (err) {
      setError(`Failed to commit note: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // ✅ FIXED: Use FormData for events (because of datetime fields)
  const createEvent = async (e) => {
    e.preventDefault();
    if (!session || !eventTitle.trim() || !eventStart || !eventEnd) return;
    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("title", eventTitle);
      formData.append("description", eventDesc);
      formData.append("start_time", eventStart);
      formData.append("end_time", eventEnd);

      const res = await fetch(`${API_BASE}/events`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to create event");
      }

      setEventTitle("");
      setEventDesc("");
      setEventStart("");
      setEventEnd("");
      fetchEvents();
    } catch (err) {
      setError(`Failed to log event: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteNote = async (id) => {
    if (!session) return;
    await fetch(`${API_BASE}/notes/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    fetchNotes();
  };

  const deleteEvent = async (id) => {
    if (!session) return;
    await fetch(`${API_BASE}/events/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${session.access_token}` },
    });
    fetchEvents();
  };

  // ✅ NEW: Update Note Status
  const updateNote = async (id, newStatus) => {
    if (!session) return;
    try {
      const res = await fetch(`${API_BASE}/notes/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!res.ok) {
        throw new Error("Failed to update status");
      }

      // Optimistic update
      setNotes((prev) =>
        prev.map((n) => (n.id === id ? { ...n, status: newStatus } : n))
      );
    } catch (err) {
      console.error(err);
      setError("Failed to update status");
      fetchNotes(); // Revert on failure
    }
  };

  const handleAskAI = async () => {
    if (!aiQuestion.trim() || !session) return;
    setAiError("");
    setAiLoading(true);
    try {
      const reply = await askAssistant(aiQuestion, session.access_token);
      setAiAnswer(reply);
      setAiQuestion("");
    } catch (err) {
      setAiError("Assistant is currently unreachable.");
    } finally {
      setAiLoading(false);
    }
  };

  const handleLogout = async () => {
    if (supabaseClient) {
      await supabaseClient.auth.signOut();
      setSession(null);
      setNotes([]);
      setEvents([]);
    }
  };

  // ---------- Auth screen ----------
  if (!session)
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-branding">
            <div className="branding-icon">
              <Layers size={24} />
            </div>
            <h2>Sync Portfolio</h2>
            <p>{isSignUp ? "Create a new secure workspace." : "Verify identity for workspace access."}</p>
          </div>
          <form onSubmit={isSignUp ? handleSignUp : handleLogin}>
            <label className="label-small">USER_ID</label>
            <input
              className="input-base"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <label className="label-small" style={{ marginTop: 16 }}>
              ACCESS_KEY
            </label>
            <input
              className="input-base"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <div className="error-badge">{error}</div>}
            <button
              className="btn-main"
              type="submit"
              disabled={loading}
              style={{ marginTop: 24 }}
            >
              {loading ? "Decrypting..." : "Open Vault"}
              <ChevronRight size={18} />
            </button>

            <div style={{ marginTop: 16, textAlign: "center" }}>
              <span
                onClick={() => {
                  setIsSignUp(!isSignUp);
                  setError("");
                }}
                style={{
                  fontSize: "12px",
                  color: "#6b7280",
                  cursor: "pointer",
                  textDecoration: "underline"
                }}
              >
                {isSignUp
                  ? "Already have an ID? Login"
                  : "Need an account? Sign Up"}
              </span>
            </div>
          </form>
        </div>
      </div>
    );

  // ---------- Main dashboard ----------
  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo">
            <Square size={18} fill="white" />
          </div>
          <span>Properties.</span>
        </div>

        <div className="nav-section">
          <h3 className="section-label">Inventory Index</h3>
          <form onSubmit={createNote}>
            <input
              className="input-base"
              placeholder="Subject"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <textarea
              className="input-base textarea"
              placeholder="Notes..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
            <button type="submit" className="btn-main" disabled={loading}>
              Commit Note
            </button>
          </form>
        </div>

        <div className="nav-section">
          <h3 className="section-label">Schedule Log</h3>
          <form onSubmit={createEvent}>
            <input
              className="input-base"
              placeholder="Event"
              value={eventTitle}
              onChange={(e) => setEventTitle(e.target.value)}
              required
            />
            <div className="time-stack">
              <div className="time-group">
                <label className="label-small">Start</label>
                <input
                  className="input-base"
                  type="datetime-local"
                  value={eventStart}
                  onChange={(e) => setEventStart(e.target.value)}
                  required
                />
              </div>
              <div className="time-group">
                <label className="label-small">End</label>
                <input
                  className="input-base"
                  type="datetime-local"
                  value={eventEnd}
                  onChange={(e) => setEventEnd(e.target.value)}
                  required
                />
              </div>
            </div>
            <textarea
              className="input-base textarea"
              placeholder="Description (optional)"
              value={eventDesc}
              onChange={(e) => setEventDesc(e.target.value)}
            />
            <button type="submit" className="btn-main" disabled={loading}>
              Log Event
            </button>
          </form>
        </div>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="user-avatar">
              {session.user.email[0].toUpperCase()}
            </div>
            <div className="user-meta">
              <p className="user-name">
                {session.user.email.split("@")[0]}
              </p>
              <p className="user-status">● OPERATOR_ACTIVE</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="btn-main"
            style={{
              background: "#f3f4f6",
              color: "#6b7280",
              fontSize: "11px",
              padding: "10px",
            }}
          >
            <LogOut size={14} /> Terminate
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="content-header">
          <div>
            <h1>Repository.</h1>
            <p className="header-subtext">
              Live synchronization with FastAPI cloud storage.
            </p>
          </div>
          <button
            onClick={() => {
              fetchNotes();
              fetchEvents();
            }}
            className="btn-sync"
            disabled={loading}
          >
            <RefreshCw size={20} className={loading ? "spinning" : ""} />
          </button>
        </header>

        {error && <div className="error-badge">{error}</div>}

        <div className="data-grid">
          {/* Notes column */}
          <section>
            <div className="column-header">
              <h3 className="section-label">Archive</h3>
              <span className="count-badge">{notes.length}</span>
            </div>
            {notes.length === 0 && (
              <p className="empty-msg">No notes yet.</p>
            )}
            {notes.map((n) => (
              <article key={n.id} className="item-card">
                <div className="card-top">
                  <h4 className="card-title">{n.title}</h4>
                  <button
                    onClick={() => deleteNote(n.id)}
                    className="btn-delete"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
                <p className="card-content">{n.content}</p>

                {/* Status Control */}
                <div className="status-control" style={{ marginTop: "12px" }}>
                  <select
                    className="status-select"
                    value={n.status || "Pending"}
                    onChange={(e) => updateNote(n.id, e.target.value)}
                    style={{
                      padding: "4px 8px",
                      borderRadius: "6px",
                      border: "1px solid #e5e7eb",
                      fontSize: "12px",
                      background: n.status === "Done" ? "#dcfce7" :
                        n.status === "In Progress" ? "#dbeafe" : "#f3f4f6",
                      color: n.status === "Done" ? "#166534" :
                        n.status === "In Progress" ? "#1e40af" : "#374151",
                      cursor: "pointer",
                      outline: "none"
                    }}
                  >
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Done">Done</option>
                  </select>
                </div>
              </article>
            ))}
          </section>

          {/* Events/Timeline column */}
          <section>
            <div className="column-header">
              <h3 className="section-label">Timeline</h3>
              <span className="count-badge">{events.length}</span>
            </div>
            {events.length === 0 && (
              <p className="empty-msg">No events yet.</p>
            )}
            {events.map((ev) => (
              <article key={ev.id} className="item-card event-card">
                <div className="card-top">
                  <div>
                    <h4 className="card-title">{ev.title}</h4>
                    <div className="time-info">
                      <Clock size={12} />
                      <span>{ev.start_time.replace("T", " ")}</span>
                    </div>
                  </div>
                  <button
                    onClick={() => deleteEvent(ev.id)}
                    className="btn-delete"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
                {ev.description && (
                  <p className="card-content" style={{ fontStyle: "italic" }}>
                    {ev.description}
                  </p>
                )}
              </article>
            ))}
          </section>

          {/* AI Assistant */}
          <section className="ai-section">
            <div className="ai-header">
              <Sparkles size={20} color="#000" />
              <h3
                className="section-label"
                style={{ marginBottom: 0, color: "#000" }}
              >
                AI Assistant
              </h3>
            </div>
            <div className="ai-box">
              <div className="ai-input-container">
                <textarea
                  className="ai-textarea"
                  placeholder="Ask about your notes or schedule..."
                  value={aiQuestion}
                  onChange={(e) => setAiQuestion(e.target.value)}
                />
                <button
                  className="btn-main ai-action-btn"
                  onClick={handleAskAI}
                  disabled={aiLoading}
                >
                  {aiLoading ? "Thinking..." : "Consult"}
                </button>
              </div>
            </div>
            {aiError && (
              <p
                style={{
                  color: "red",
                  fontSize: "12px",
                  marginTop: "12px",
                }}
              >
                {aiError}
              </p>
            )}
            {aiAnswer && (
              <div className="ai-response">
                <div className="ai-response-label">
                  <MessageSquare size={12} /> Assistant Output
                </div>
                <div className="ai-response-text">{aiAnswer}</div>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
