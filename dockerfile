# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask flask-sqlalchemy mysql-connector-python

# Expose the Flask port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run"]
