# Medical Chatbot: A Medical Chatbot

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Code Size](https://img.shields.io/github/languages/code-size/khulalit/MediBot)
![Dependencies](https://img.shields.io/badge/dependencies-up--to--date-brightgreen)

## Description
Medical Chatbot is a conversational AI chatbot designed to provide information about medical conditions, symptoms, and treatments. It is built using Python, Streamlit for the frontend, FastAPI for the backend, and LangChain/LangGraph for the conversational logic.

## Features
*   **Interactive Chat Interface:** A user-friendly web interface for interacting with the chatbot.
*   **Medical Information:** Provides information on a wide range of medical topics.
*   **Disclaimer:** Includes a disclaimer in every response to advise users to consult with a healthcare professional.
*   **Clear Conversation History:** Allows users to clear the conversation history.
*   **Download Conversation:** Download your chat as a text file with a timestamped filename for easy organization.
*   **Symptom Checker:** Enter symptoms and get possible conditions.
*   **Feedback Submission:** Submit feedback on chatbot answers.
*   **View Conversation History:** See all previous conversations in the session.

## Getting Started

### Prerequisites
*   Python 3.7+
*   An OpenAI API key

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Medical Chatbot
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your OpenAI API key:**
    Create a `.env` file in the root directory of the project and add your OpenAI API key as follows:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    ```

### Running the Application
1.  **Start the backend server:**
    ```bash
    python main.py
    ```
2.  **In a new terminal, start the frontend application:**
    ```bash
    streamlit run frontend.py
    ```
3.  **Open your web browser and navigate to `http://localhost:8501`

## Project Structure
```
.
├── api.py              # Defines the FastAPI backend application.
├── frontend.py         # Defines the Streamlit frontend application.
├── graph.py            # Defines the LangGraph conversational graph.
├── main.py             # The entry point for the backend server.
├── nodes.py            # Contains the nodes for the LangGraph graph.
├── requirements.txt    # Lists the Python dependencies for the project.
├── state.py            # Defines the conversation state.
└── README.md           # This file.
```

## Dependencies
*   fastapi
*   uvicorn
*   langchain
*   langchain-openai
*   streamlit
*   requests
*   langgraph

## Disclaimer
This chatbot is an AI assistant and not a real doctor. Please consult with a healthcare professional for any medical advice. The information provided by this chatbot is for informational purposes only and should not be considered as medical advice.
# MediBot
