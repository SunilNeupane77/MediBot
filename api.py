from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import app
from state import ConversationState
from typing import Any
import sqlite3

api = FastAPI()

# Allow CORS for frontend communication
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite setup
DB_PATH = "chatbot.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    messages TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS symptom_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    symptoms TEXT,
    conditions TEXT
)
""")
conn.commit()

class ChatInput(BaseModel):
    state: Any  # Accept any dict-like state

class SymptomCheckInput(BaseModel):
    symptoms: str

@api.post("/chat")
def chat(chat_input: ChatInput) -> dict:
    # Invoke the graph
    updated_state = app.invoke(chat_input.state)
    # Save to history in SQLite
    import datetime
    c.execute(
        "INSERT INTO conversation_history (timestamp, messages) VALUES (?, ?)",
        (datetime.datetime.now().isoformat(), str(updated_state["messages"]))
    )
    conn.commit()

    # Log the structure of the updated state for debugging
    print("Updated state from graph:", updated_state)

    # The graph's output might be the state itself or nested.
    # We ensure that we return only the ConversationState dictionary.
    if isinstance(updated_state, dict) and "messages" in updated_state:
        return updated_state
    elif isinstance(updated_state, dict) and "__end__" in updated_state:
        # In some versions of langgraph, the final state is under the "__end__" key
        return updated_state.get("__end__", {})
    else:
        # Handle other possible nested structures if necessary
        # For now, we'll assume it might be directly nested under a key like 'state'
        # or is the root object. If the error persists, the print statement will guide us.
        return updated_state

@api.get("/")
def read_root():
    return {"Hello": "World"}

@api.get("/history")
def get_history():
    c.execute("SELECT timestamp, messages FROM conversation_history ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    return {"history": [{"timestamp": r[0], "messages": r[1]} for r in rows]}

@api.post("/symptom-check")
def symptom_check(input: SymptomCheckInput):
    # Simple static mapping for demo; replace with LLM call for real use
    symptom_map = {
        "fever": ["Flu", "COVID-19", "Common Cold"],
        "headache": ["Migraine", "Tension Headache", "Dehydration"],
        "cough": ["Bronchitis", "Asthma", "Allergy"]
    }
    found = []
    for key, conds in symptom_map.items():
        if key in input.symptoms.lower():
            found.extend(conds)
    if not found:
        found = ["No common conditions found. Please consult a doctor."]
    # Save to SQLite
    import datetime
    c.execute(
        "INSERT INTO symptom_checks (timestamp, symptoms, conditions) VALUES (?, ?, ?)",
        (datetime.datetime.now().isoformat(), input.symptoms, str(list(set(found))))
    )
    conn.commit()
    return {"possible_conditions": list(set(found))}

@api.get("/symptom-checks")
def get_symptom_checks():
    c.execute("SELECT timestamp, symptoms, conditions FROM symptom_checks ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    return {"checks": [{"timestamp": r[0], "symptoms": r[1], "conditions": r[2]} for r in rows]}