# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file if exists (optional)
# COPY requirements.txt .

# Install Flask and other dependencies directly
RUN pip install --no-cache-dir flask

# Copy all files from your project folder to container
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Set environment variable to disable Python buffering (for better logging)
ENV PYTHONUNBUFFERED=1

# Run the Flask application
CMD ["python", "app.py"]
