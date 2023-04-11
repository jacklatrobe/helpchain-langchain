# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory to /app
WORKDIR /langchain-service

# Copy the current directory contents into the container at /app
ADD /langchain-service/. /langchain-service

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME LangChain

# Run app.py when the container launches
CMD ["python", "main.py"]