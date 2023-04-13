## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/language-backend.py

import openai
import os
import validators
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.agents import load_tools, Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# I've had hella trouble with env files, so being strict on these checks
if os.path.isfile("helpchain.env"):
    load_dotenv("helpchain.env")
else:
    raise FileNotFoundError("helpchain.env file not located")

# intelligent_response - entry point and wrapper function
def intelligent_response(query):
    if os.environ.get("OPENAI_API_KEY") is None:
        return "OpenAI API key error"
    if os.environ.get("OPENWEATHERMAP_API_KEY") is None:
        return "OpenWeatherMap API key error"

    prompt = "Create a well-writen, well-referenced and factually accurate response to the query. Make your response at least three well-written paragraphs. Include relevant URLs where you know them. Their query was:\n{}".format(query)
    prompt_tokens = int(len(prompt) * 4)
    if(prompt_tokens > 2000):
        return "Error generating response - prompt was too long"
    control_llm = OpenAI(temperature=0.3, max_tokens=(4000-prompt_tokens))
    tools = [
        Tool(
            name="Intermediate Answer",
            func=researcher,
            description="Useful for when you need to look up additional information, documents, URLs or other research to provide an answer. This tool accepts the entire query as text and returns relevant research. This tool can look up URLs"
        )
    ]   

    agent = initialize_agent(tools, control_llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)

    result = agent.run(prompt)

    if is_good_response(query,compressor(result)):
        return result
    else:
        prompt = compressor("Our system was given this prompt:\n{query}\n\nOur system produced the following output:\n{result}\n\nThe response was not accurate. Try again".format(query=query,result=result))
        return agent.run(prompt)
    
# researcher - Agent to handle all external calls and research
def researcher(query):
    wikipedia = WikipediaAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    prompt="Use the available tools to generate a succinct research summary which includes URLs where you know them. The research question is: {}".format(query)
    prompt_tokens = int(len(prompt) * 4)
    if(prompt_tokens > 2000):
        return "Error generating response - prompt was too long"
    control_llm = OpenAI(temperature=0.3, max_tokens=(4000-prompt_tokens))
    tools = [
        Tool(
            name="Solve complex problems with frameworks",
            func=framework,
            description="This tool uses knowledge of problem solving frameworks such as agile, systems thinking and communications theory to suggest structured steps that could be followed to solve more complex challenges. Submit the whole initial query and any relevant context to this tool."
        ),
        Tool(
            name="Search Wikipedia for articles",
            func=wikipedia.run,
            description="Useful for searching for general information about people, places, concepts and historical events. The input for this tool should be in the format of the specific encyclopedia article you are looking for"
        ),
        Tool(
            name="Lookup current weather data",
            func=weather.run,
            description="Useful for when you need to search for the current weather in a specific location. The input for this tool must be in the format 'CITY, COUNTRY'"
        ),
        Tool(
            name="Extract a location from a query",
            func=smart_location_extractor,
            description="Useful for extracting a specific location for use in the Weather Lookup tool when given a general area or broad location by a user. Output is in the format 'CITY, COUNTRY'"
        ),
        Tool(
            name="Explain HelpChain and the Latrobe Consulting Group",
            func=latrobe_consulting,
            description="Answers questions like 'Who are you?' and 'What is this?' and 'Who built this?'. This current platform (HelpChain) was built by the Latrobe Consulting Group. This tool provides information about the Latrobe Consulting Group (LCG). Always provide the URL: https://latrobe.group/"
        ),
        Tool(
            name="Opens a single webpage, article or document and gets the LLM to convert and summarise it",
            func=read_the_docs,
            description="Useful for loading single webpage, article or document given a single URL and summarising it's content. Useful for reading customer docs, developer docs, product documentation when we know the link. The input for this tool must be in URL format similar to 'http://example.com/'. "
        )
    ]
    agent = initialize_agent(tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run(prompt)
    return compressor(response)

# smart_location_extractor - Extract a location from a query (For OpenWeatherMap)
def smart_location_extractor(query):
    control_llm = OpenAI(temperature=0)
    text = "In a format similar to 'London,GB', extract the location from the following user query:{}".format(query)
    return control_llm(text)

# latrobe_consulting - Explain what HelpChain is and who built it
def latrobe_consulting(query):
    return "Technology Strategy, Cloud & DevOps, Engineering Culture - The Latrobe Consulting Group delivers holistic solutions to your technology and product challenges. Latrobe Consulting Group (LCG) is an Australian-based technology and business advisory company. We take a holistic approach to helping our clients solve problems in their business, drawing on our extended network of professionals for advice in areas such as Technology Strategy & Operations, Product Development and Engineering Culture to provide solutions that are tailored for your business. Get in touch at: https://latrobe.group or contact jack@latrobe.group"

# is_good_response - Check if your response is high quality, or try to improve it more
def is_good_response(initial, planned):
    agent_prompt="Generated text:\n{initial}\n\nOriginal question or task:\n{planned}\n\nAnswering only Yes or No, does the generated text answer the question, and is it accurate?".format(initial=initial, planned=planned)
    control_llm = OpenAI(temperature=0)
    result = control_llm(agent_prompt)
    if result == "No":
        return False
    else:
        return True

# framework - Solve complex problems with frameworks
def framework(query):
    llm = OpenAI(temperature=0.8, max_tokens=2000)
    prompt = PromptTemplate(
        input_variables=["query"],
        template="The following step is a task that a user is trying to do while trying to solve a challenge or answer a question. Use your knowledge of problem solving frameworks such as agile, systems thinking and communications theory to suggest structured steps that the user could follow to solve the problem, being as descriptive as possible.\n\nTheir challenge is: {query}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return compressor(chain.predict(query=query))

# read_the_docs - Opens a single webpage, article or document and gets the LLM to convert and summarise it
def read_the_docs(query):
    if not validators.url(query):
        return "This is not a valid URL - unable to look up webpage, article or document"
    f = requests.get(query)
    content = f.text
    llm = OpenAI(temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["content"],
        template="The following is the content of a webpage. Convert it into well formated human readable text, taking specific care to preserve any code examples or step by step technical instructions. \n\nThe content of the page is:\n{query}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return compressor(chain.predict(content=content))

def compressor(text):
    prompt = "compress the following text in a way that is lossless but results in the minimum number of tokens which could be fed into an LLM like yourself as-is and produce the same output. feel free to use multiple languages, symbols, other up-front priming to lay down rules. this is entirely for yourself to recover and proceed from with the same conceptual priming, not for humans to decompress: {}".format(text)
    prompt_tokens=int(len(prompt) * 4)
    if(prompt_tokens > 2000):
        return "Error generating response - prompt was too long"
    compressor_llm = OpenAI(temperature=0, max_tokens=(4000-prompt_tokens))
    return compressor_llm(prompt)

def summariser(text):
    compressor_llm = OpenAI(temperature=0)
    return compressor_llm("Summarise: {}".format(text))