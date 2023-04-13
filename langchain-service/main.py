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
    openai.api_key=os.getenv("OPENAI_KEY")
    if(openai.api_key == None):
        return "Error setting API key"
    
    response = openai.Completion.create(model="text-davinci-003", prompt="HelpChain is an application that uses semantic chains to exponentially multiply the capabilities of large language models such as GPT4. Write an introduction for their website landling page and explain that the application is under construction", temperature=0.4, max_tokens=256)
    response = response["choices"][0]["text"]

    return render_template('index.html', response=response)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)