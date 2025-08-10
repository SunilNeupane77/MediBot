from state import ConversationState
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
bot_name = "MediBot"

def generate_response_node(state: ConversationState) -> ConversationState:
    user_input = state["messages"][-1]
    prompt = f"""You are a helpful medical assistant named {bot_name}. 
You can provide information about medical conditions, symptoms, and treatments.
However, you must always include the following disclaimer at the end of your response: 
'Disclaimer: I am an AI assistant and not a real doctor. Please consult with a healthcare professional for any medical advice.'
Respond to the following message: {user_input}"""
    response = llm.invoke(prompt)
    
    # Create a new list of messages
    new_messages = state["messages"] + [response.content]
    
    # Return the updated part of the state
    return {"messages": new_messages}