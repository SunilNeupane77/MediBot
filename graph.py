from langgraph.graph import StateGraph, END
from state import ConversationState
from nodes import generate_response_node

graph = StateGraph(ConversationState)

graph.add_node("generate_response", generate_response_node)

graph.set_entry_point("generate_response")
graph.add_edge("generate_response", END)

app = graph.compile()