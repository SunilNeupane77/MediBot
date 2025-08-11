# Medical Chatbot

## Description
This is a conversational AI chatbot designed to provide information about medical conditions, symptoms, and treatments. It is built using Streamlit for the frontend, FastAPI for the backend API, and LangChain/LangGraph for the conversational logic.

## Features
*   Interactive chat interface
*   Medical information retrieval
*   Disclaimer for medical advice

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ai
    ```
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to install `pip` first if it's not available in your virtual environment.)*

## How to Run

1.  **Start the backend server:**
    ```bash
    python3 main.py &
    ```
2.  **Start the frontend application:**
    ```bash
    streamlit run frontend.py &
    ```
3.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8501` (or the address provided by Streamlit).

## Technologies Used
*   Python
*   Streamlit
*   FastAPI
*   LangChain
*   LangGraph
*   OpenAI (for LLM)

## Disclaimer
This chatbot is an AI assistant and not a real doctor. Please consult with a healthcare professional for any medical advice. The information provided by this chatbot is for informational purposes only and should not be considered as medical advice.

## Docker Instructions

# Build and push the backend image
```bash
docker build -f backend.Dockerfile -t <your-dockerhub-username>/medical-chatbot-backend:latest .
docker push <your-dockerhub-username>/medical-chatbot-backend:latest
```

# Build and push the frontend image
```bash
docker build -f frontend.Dockerfile -t <your-dockerhub-username>/medical-chatbot-frontend:latest .
docker push <your-dockerhub-username>/medical-chatbot-frontend:latest
```

# To run with docker-compose using published images:
```bash
docker-compose up
```
# MediBot
