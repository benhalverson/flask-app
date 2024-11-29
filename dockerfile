# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development 
# Enable development mode for auto-reload

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug" ]
