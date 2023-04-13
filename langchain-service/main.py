## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask, render_template
from dotenv import load_dotenv
import os
import socket
import openai


load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello():
    openai.api_key = os.environ.get("OPENAI_KEY")
    response = openai.Completion.create(model="text-davinci-003", prompt="Write a quote of the day, wrapped in HTML <div> tags", temperature=0.7, max_tokens=200)
    response = response["choices"][0]["text"]

    return render_template('index.html', response=response)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)