
# Base image
FROM python:3.12-slim

# Working folder inside the container
WORKDIR /app

# Install the dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Streamlit runs on port 8501
EXPOSE 8501

# Start the Streamlit app and make it reachable from outside the container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
