# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory to /langchain-service
WORKDIR /web-scraper

# Copy the current directory contents into the container at /langchain-service
ADD . /web-scraper

# Build the playwright web scraper
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y graphviz
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install playwright==1.20.0
RUN playwright install-deps chromium
RUN playwright install chromium

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=WebScraper

# Run app.py when the container launches
CMD ["python", "main.py"]