import streamlit as st
import requests
import os
import io
import json

# Define the backend URL, default to localhost for local dev
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Set the title of the web app
st.title("Medical Chatbot")

# Sidebar with a button to clear the conversation
with st.sidebar:
    st.title("Options")
    if st.button("Clear History"):
        st.session_state.conversation = {
            "messages": ["Hello! I'm MediBot, your medical assistant. How can I help you today?"],
        }
        st.rerun()

    st.title("About")
    st.info(
        "This is a medical chatbot that can answer your questions about "
        "medical conditions, symptoms, and treatments."
    )

    st.markdown("---")
    st.markdown("Developed by Sunil Neupane")

    # Download conversation button
    if st.button("Download Conversation"):
        chat_text = "\n".join(st.session_state.conversation["messages"])
        st.download_button("Download Chat", chat_text, file_name="chat_history.txt")

    # Symptom checker UI
    st.title("Symptom Checker")
    symptom_input = st.text_input("Enter your symptoms (comma separated):")
    if st.button("Check Symptoms") and symptom_input:
        resp = requests.post(f"{BACKEND_URL}/symptom-check", json={"symptoms": symptom_input})
        if resp.ok:
            st.success("Possible conditions: " + ", ".join(resp.json()["possible_conditions"]))
        else:
            st.error("Error checking symptoms.")

    # Conversation history UI
    st.title("Conversation History")
    if st.button("Show History"):
        resp = requests.get(f"{BACKEND_URL}/history")
        if resp.ok:
            st.write(resp.json()["history"])
        else:
            st.error("Could not fetch history.")

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

# Feedback form below chat
st.markdown("---")
st.subheader("Feedback")
feedback_text = st.text_area("Your feedback about the last answer:")
if st.button("Submit Feedback") and feedback_text:
    last_message = st.session_state.conversation["messages"][-1] if st.session_state.conversation["messages"] else ""
    resp = requests.post(f"{BACKEND_URL}/feedback", json={"message": last_message, "feedback": feedback_text})
    if resp.ok:
        st.success("Thank you for your feedback!")
    else:
        st.error("Failed to submit feedback.")
