# Use the official Python image as the base image
FROM python:3.11-slim

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

# Command to start the Flask app
CMD ["python", "./src/main_server.py"]
