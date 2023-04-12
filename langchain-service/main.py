## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask
import os
import socket
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_KEY")

@app.route("/")
def hello():
    try:
        response = openai.Completion.create(model="text-davinci-003", prompt="Write a HTML and CSS page that announces this site is under construction, which includes a random quote of the day in the centre of the page", temperature=0.3, max_tokens=1024)
        response = response["choices"][0]["text"]
    except Exception as ex:
        response = "Error in GPT API: {}".format(ex)

    return response

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)