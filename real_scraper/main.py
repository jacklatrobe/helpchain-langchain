## RealScraper - takes the lessons learned from LangChain to build an AI-powered rental advocate
## File: real_scraper/main.py

from flask import Flask, render_template, request
from language_backend import intelligent_response

app = Flask(__name__)

@app.route("/")
def hello():
    query = request.args.get('query')
    if request.args.get('query') is None:
        return render_template("index.html")
    response = intelligent_response(query)
    return render_template("index.html", response=response)

@app.route("/health")
def healthcheck():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)