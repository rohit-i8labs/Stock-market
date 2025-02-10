# Use the smallest official Python runtime
FROM python:3.11.11-alpine

# Set environment variables for Python to optimize runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium-browser \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Chromium and ChromeDriver
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver 

# Copy only requirements.txt first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
