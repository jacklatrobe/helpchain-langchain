# We need an OpenAI API key for the solution to work
ARG OPENAIKEY

# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory to /langchain-service
WORKDIR /langchain-service

# Copy the current directory contents into the container at /langchain-service
ADD /langchain-service/. /langchain-service

# Overwrite the python .env file for the /langchain-service
RUN echo "OPENAI_KEY=${OPENAIKEY}" > /langchain-service/.env

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=LangChain

# Run app.py when the container launches
CMD ["python", "main.py"]