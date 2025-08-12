from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import app
from state import ConversationState
from typing import Any

api = FastAPI()

# Allow CORS for frontend communication
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for conversation history and feedback (for demo)
conversation_history = []
feedback_list = []

class ChatInput(BaseModel):
    state: Any  # Accept any dict-like state

class SymptomCheckInput(BaseModel):
    symptoms: str

class FeedbackInput(BaseModel):
    message: str
    feedback: str

@api.post("/chat")
def chat(chat_input: ChatInput) -> dict:
    # Invoke the graph
    updated_state = app.invoke(chat_input.state)
    # Save to history
    conversation_history.append(updated_state)

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
    return {"history": conversation_history}

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
    return {"possible_conditions": list(set(found))}

@api.post("/feedback")
def submit_feedback(input: FeedbackInput):
    feedback_list.append({"message": input.message, "feedback": input.feedback})
    return {"status": "success", "msg": "Feedback received. Thank you!"}