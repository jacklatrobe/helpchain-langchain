## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask, render_template
from dotenv import load_dotenv
import os
import socket
import openai

app = Flask(__name__)

@app.route("/")
def hello():
    load_dotenv()
    openai.api_key=os.getenv("OPENAI_KEY")
    if(openai.api_key == None):
        return "Error setting API key"
    response = openai.Completion.create(model="text-davinci-003", prompt="Generate an inspirational quote that is funny because it is attributed to the wrong person. Examples include: 'If at first you don't succeed, try and try again - Lee Harvey Oswald' and 'If at first you don't succeed, give up, fail fast and move on - Yoda'", temperature=0.4, max_tokens=256)
    response = response["choices"][0]["text"]

    return render_template('index.html', response=response)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)