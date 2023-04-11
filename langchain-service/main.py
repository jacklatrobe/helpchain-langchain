## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask
import os
import socket
import langchain
import openai

app = Flask(__name__)

@app.route("/")
def hello():
    # Get OpenAI secret

    openai.api_key = os.getenv("OPENAI_KEY")

    html = openai.Completion.create(model="gpt-3.5-turbo", prompt="Return HTML code that displays a simple under construction page with a cute, randomly generated message from GPT in the middle", temperature=0.1, max_tokens=1024)

    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)