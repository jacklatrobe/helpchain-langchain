## Helpchain-Langchain: Microservices components for the langchain component of the GPT solution
## File: langchain-service/language-backend.py

import openai
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper
from langchain.agents import load_tools, Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

load_dotenv()

def intelligent_response(query):
    openai.api_key=os.getenv("OPENAI_KEY")


    wikipedia = WikipediaAPIWrapper()
    weather = OpenWeatherMapAPIWrapper()
    control_llm = OpenAI(temperature=0.1)
    tools = [
    Tool(
        name="Intermediate Answer",
        func=wikipedia.run,
        description="Useful for searching for general information about people, places, concepts and historical events. The input for this tool should be in the format of the specific encyclopedia article you are looking for"
    ),
    Tool(
        name="Weather Lookup",
        func=weather.run,
        description="Useful for when you need to search for the current weather in a specific location. The input for this tool must be in the format 'CITY, COUNTRY'"
    ),
    Tool(
        name="Location Extractor",
        func=smart_location_extractor,
        description="Useful for extracting a specific location for use in the Weather Lookup tool when given a general area or broad location by a user. Output is in the format 'CITY, COUNTRY'"
    ),
    Tool(
        name="Latrobe Consulting Explainer",
        func=latrobe_consulting,
        description="This current platform (HelpChain) was built by the Latrobe Consulting Group. This tool provides information about the Latrobe Consulting Group (LCG)"
    ),
    Tool(
        name="Nonsense Filter",
        func=nonsense,
        description="When a user prompt doesn't make any sense, this tool attempts to clean it up or return a prompt back to them suggesting how they could phrase their query better."
    )
    ]   

    agent = initialize_agent(tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    return agent.run(query)

def smart_location_extractor(query):
    control_llm = OpenAI(model_name="text-curie-001", temperature=0)
    text = "In a format similar to 'London,GB', extract the location from the following user query:{}".format(query)
    return control_llm(text)

def latrobe_consulting(query):
    return "Technology Strategy, Cloud & DevOps, Engineering Culture - The Latrobe Consulting Group delivers    holistic solutions to your technology challenges. Latrobe Consulting Group (LCG) is an Australian-based technology and business advisory company. We take a holistic approach to helping our clients solve problems in their business, drawing on our extended network of professionals for advice in areas such as Technology Strategy & Operations, Product Development and Engineering Culture to provide solutions that are tailored for your business. Get in touch at: https://latrobe.group or contact jack@latrobe.group"

def nonsense(query):
    control_llm = OpenAI(temperature=0.3)
    return "The user has submitted a query that doesn't make sense. Try to clean up what they are asking, or if you cannot make sense of it still, return some helpful advice on how they could phrase it better."