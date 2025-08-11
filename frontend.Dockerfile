# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Add a label to describe the Dockerfile
LABEL description="Frontend for the Medical Chatbot"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend code into the container at /app
COPY frontend.py .

# Environment variables
ENV BACKEND_URL=http://backend:8000

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "frontend.py", "--server.port", "8501", "--server.address", "0.0.0.0"]