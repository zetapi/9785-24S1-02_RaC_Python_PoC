# Use the official Python image as the base image
FROM python:3.9-slim

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor curl

# Install ollama package
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory in the container
WORKDIR .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Copy Supervisor configuration file
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Command to start Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
