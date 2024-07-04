# Use the official Python runtime as a parent image
FROM python:3.10.11-slim

# Install necessary system dependencies for Tkinter
# RUN apt-get update && apt-get install -y python3-tk tk-dev libffi-dev

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Set the default command to run the Python script
ENTRYPOINT ["python", "./ifap_decoder.py"]

# Define default command
CMD ["./input_videos/08fd33_4.mp4"]
