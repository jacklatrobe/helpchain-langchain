## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask, render_template
import os
import socket
import openai

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        openai.api_key = os.environ.get("OPENAI_KEY")
        response = openai.Completion.create(model="text-davinci-003", prompt="Write a quote of the day, wrapped in HTML <div> tags", temperature=0.7, max_tokens=200)
        response = response["choices"][0]["text"]
    except Exception as ex:
        response = "Error in GPT API: {}".format(ex)

    return render_template('index.html', response)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)