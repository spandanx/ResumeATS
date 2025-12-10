# Python base image
# FROM python:3.10-slim-buster
FROM python:3.10.4-buster

# Set the working directory inside the container
WORKDIR /resume-ats-app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "ui.py", "--server.sslKeyFile", "certs/key.pem", "--server.sslCertFile", "certs/cert.pem"]