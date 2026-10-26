
# Base image
FROM python:3.12-slim

# Working folder inside the container
WORKDIR /app

# Install the dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files (app.py and the saved model)
COPY . .

# The API listens on port 7860
EXPOSE 7860

# Start the Flask app with gunicorn (2 workers) on port 7860
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:extraalearn_api"]
