import streamlit as st
import requests
import os

# Define the backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Set the title of the web app
st.title("Medical Chatbot")

# Initialize the conversation state in Streamlit's session state
if "conversation" not in st.session_state:
    st.session_state.conversation = {
        "messages": ["Hello! I'm MediBot, your medical assistant. How can I help you today?"],
    }

# Display the conversation history
for message in st.session_state.conversation["messages"]:
    with st.chat_message("assistant"):
        st.markdown(message)

# Get user input
if user_input := st.chat_input("Type your message here..."):
    # Add user input to the conversation history
    st.session_state.conversation["messages"].append(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send the user input to the backend
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={
            "state": st.session_state.conversation,
        }
    )

    # Update the conversation state with the response from the backend
    st.session_state.conversation = response.json()

    # Display the latest message from the backend, with a check
    if "messages" in st.session_state.conversation and st.session_state.conversation["messages"]:
        with st.chat_message("assistant"):
            st.markdown(st.session_state.conversation["messages"][-1])
    else:
        with st.chat_message("assistant"):
            st.error("Error: No messages received from the backend.")