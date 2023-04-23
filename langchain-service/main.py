## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/main.py

from flask import Flask, render_template, request
from datetime import datetime
from language_backend import handle_query
from telstra_backend import handle_telstra_query

app = Flask(__name__)

@app.route("/")
def hello():
    query = request.args.get('query')
    if request.args.get('query') is None:
        return example_chat_response()
    else:
        return prepared_chat_response(query)
    
@app.route("/telstra")
def telstra():
    query = request.args.get('query')
    if request.args.get('query') is None:
        return example_telstra_response()
    else:
        return prepared_telstra_response(query)

@app.route("/info")
def site_info():
    return "HelpChain 2023 - by <a href='https://latrobe.group/'>https://latrobe.group/</a><br><p>Source code: <a href='https://github.com/jacklatrobe/helpchain-langchain'>GitHub</a></p>"

@app.route("/health")
def healthcheck():
    return "OK"

def example_chat_response():
    response = """
        <div class="msg left-msg">
            <div class="msg-img"><img src='/static/img/bot_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">HelpChain</div>
                <div class="msg-info-time">HH:MM</div>
                </div>

                <div class="msg-text">
                Hi, welcome to HelpChain, an LLM proof-of-concept from the <a href='https://latrobe.group/'>Latrobe Consulting Group</a>! Go ahead and send me a message. 😄
                </div>
            </div>
            </div>

            <div class="msg right-msg">
            <div class="msg-img"><img src='/static/img/user_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">User</div>
                <div class="msg-info-time">HH:MM</div>
                </div>

                <div class="msg-text">
                Enter your query or question below to get started!
                </div>
            </div>
        </div>
        """
    return render_template("chat.html", response=response)

def prepared_chat_response(query):
    msg_sent_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot_response = handle_query(query)
    msg_rec_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    response="""
        <div class="msg right-msg">
            <div class="msg-img"><img src='/static/img/user_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">User</div>
                <div class="msg-info-time">{msg_sent_time}</div>
                </div>
                <div class="msg-text">
                    {query}
                </div>
            </div>
            </div>

            <div class="msg left-msg">
            <div class="msg-img"><img src='/static/img/bot_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">HelpChain</div>
                <div class="msg-info-time">{msg_rec_time}</div>
                </div>

                <div class="msg-text">
                    {response}
                </div>
            </div>
        </div>
    """.format(msg_sent_time=msg_sent_time, query=query, msg_rec_time=msg_rec_time, response=bot_response)
    return render_template("chat.html", response=response)

def example_telstra_response():
    response = """
        <div class="msg left-msg">
            <div class="msg-img"><img src='/static/img/bot_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">Telstra Bot</div>
                <div class="msg-info-time"></div>
                </div>

                <div class="msg-text">
                Hi, welcome to the Telstra Search Bot, an GPT proof of concept from the <a href='https://latrobe.group/'>Latrobe Consulting Group</a> 😄
                </div>
            </div>
            </div>

            <div class="msg right-msg">
            <div class="msg-img"><img src='/static/img/user_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">User</div>
                <div class="msg-info-time"></div>
                </div>

                <div class="msg-text">
                Enter your query or question below and the bot will search Telstra.com.au for answers!
                </div>
            </div>
        </div>
        """
    return render_template("telstra.html", response=response)

def prepared_telstra_response(query):
    msg_sent_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot_response = handle_telstra_query(query)
    msg_rec_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    response="""
        <div class="msg right-msg">
            <div class="msg-img"><img src='/static/img/user_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">User</div>
                <div class="msg-info-time">{msg_sent_time}</div>
                </div>
                <div class="msg-text">
                    {query}
                </div>
            </div>
            </div>

            <div class="msg left-msg">
            <div class="msg-img"><img src='/static/img/bot_logo.png'></div>
            <div class="msg-bubble">
                <div class="msg-info">
                <div class="msg-info-name">Telstra Bot</div>
                <div class="msg-info-time">{msg_rec_time}</div>
                </div>

                <div class="msg-text">
                    {response}
                </div>
            </div>
        </div>
    """.format(msg_sent_time=msg_sent_time, query=query, msg_rec_time=msg_rec_time, response=bot_response)
    return render_template("telstra.html", response=response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)