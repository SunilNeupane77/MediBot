from fastapi import FastAPI
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

class ChatInput(BaseModel):
    state: Any  # Accept any dict-like state

@api.post("/chat")
def chat(chat_input: ChatInput) -> dict:
    # Invoke the graph
    updated_state = app.invoke(chat_input.state)

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