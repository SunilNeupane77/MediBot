
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Add a label to describe the Dockerfile
LABEL description="Backend for the Medical Chatbot"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
