# Use an official Python image as the base image  
FROM python:3.12-slim  

# Set the working directory  
WORKDIR /app  

# Create and activate a virtual environment  
RUN python -m venv venv  
ENV PATH="/app/venv/bin:$PATH"  

# Install dependencies  
COPY requirements.txt /app/requirements.txt  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the application code into the container  
COPY . /app  

# Expose the port the server will run on  
EXPOSE 8000  

# Run Uvicorn using the python in the virtual environment  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  
