## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask, render_template, request
from language_backend import intelligent_response

app = Flask(__name__)

@app.route("/")
def hello():
    query = request.args.get('query')
    if request.args.get('query') is None:
        return render_template("index.html")
    response = intelligent_response(query)
    response = response.replace("\n","<br />\n")
    return render_template("index.html", response=response, query=query)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)