# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install dependencies for Selenium, Chrome, and Chromedriver
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    libx11-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxi-dev \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libgconf-2-4 \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libnspr4 \
    libxrandr2 \
    libgbm1 \
    libu2f-udev \
    libpango-1.0-0 \
    xdg-utils \
    --no-install-recommends

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; \
    apt-get update; apt-get install -f -y

# Install the chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the application using Uvicorn as the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]