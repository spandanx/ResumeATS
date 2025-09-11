# Use a lightweight Python base image
# python:3.11-alpine
# python:3.9-slim-buster
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /resume-ats-app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8501

# Command to run the FastAPI application with Uvicorn
CMD ["streamlit", "run", "ui.py"]