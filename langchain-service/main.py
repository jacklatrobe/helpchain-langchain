## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    html = """Welcome to the container hosting: {name}!
    Current instance hostname: {hostname}"""
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)