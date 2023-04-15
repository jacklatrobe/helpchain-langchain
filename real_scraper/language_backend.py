## RealScraper - takes the lessons learned from LangChain to build an AI-powered rental advocate
## File: real_scraper/language-backend.py

import openai
import os
import validators
import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain import LLMMathChain
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.utilities import WikipediaAPIWrapper

# I've had hella trouble with env files, so being strict on these checks
env_loc = "vars.env"
if os.path.isfile(env_loc):
    load_dotenv(env_loc)
else:
    raise FileNotFoundError("{} file not located".format(env_loc))

# format_response - wraps language backend responses in HTML before return to flask
def format_response(initial_query, response, notes = None):
    ## todo
    return response

# roundup - Rounds integers up to the nearest 100 for token handling
def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

# intelligent_response - entry point and wrapper function
def intelligent_response(query):
    if os.environ.get("OPENAI_API_KEY") is None:
        return "OpenAI API key error"
    
    prompt="Write a list of rental properties that meet the criteria given. Provide at least three options. Include the bedrooms, bathrooms, a short description and their URL for each listing. Format the output as HTML. The user has provided the following requirements: {}".format(query)
    token_llm = OpenAI()
    prompt_tokens = int(400 + (1.25 * token_llm.get_num_tokens(prompt)))
    print(prompt_tokens)
    control_llm = OpenAI(temperature=0.2, frequency_penalty=0.1, presence_penalty=0.1, max_tokens = (3000-prompt_tokens))
    wikipedia = WikipediaAPIWrapper()
    llm_math_chain = LLMMathChain(llm=control_llm)
    custom_tools = [
        Tool(
            name="web_scraper",
            func=requests_filtered,
            description="A portal to the internet. Use this when you need to get specific content from any website. Input should be a specific url, and the output will be all the text on that page."
        ),
        Tool(
            name="listing_parser",
            func=listing_parser,
            description="Use this to retrieve a list of properties from a known valid rental listing URL. Only accepts a valid URL to a rental listing page, and will return a formatted list of the properties on that page."
        ),
        Tool(
            name="wikipedia",
            func=wikipedia.run,
            description="A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, historical events, or other subjects. Input should be a search query."
        ),
        Tool(
            name="calculator",
            func=llm_math_chain.run,
            description="Useful for when you need to answer questions about math or calculate math answers."
        ),
        Tool(
            name="providers",
            func=rental_listing_providers,
            description="Useful for when you need to find a website to search for rental listings or a real estate"
        )
    ]
    
    agent = initialize_agent(custom_tools, control_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run(prompt)
    return response

def requests_filtered(query):
    # description: A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be all the text on that page.
    if not validators.url(query):
        return "This is not a valid URL, unable to lookup document - please try again with a different URL"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    f = requests.get(query, headers=headers)
    html = BeautifulSoup(f.content, "html.parser")
    body = " ".join(html.body.text.split())
    response = "Page tite: {}\nPage URL: {}\nPage Content: {}".format(html.title.prettify, query, body)
    return response

def listing_parser(query):
    # description: A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be all the text on that page.
    if not validators.url(query):
        return "The value you have provided does not appear to be a valid URL to a rental listing page - please try again with a different URL"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    f = requests.get(query, headers=headers)
    html = BeautifulSoup(f.content, "html.parser")
    body = " ".join(html.body.text.split())
    token_llm = OpenAI()
    prompt_tokens = int(400 + 1.25 * token_llm.get_num_tokens(body))
    llm=OpenAI(temperature=0.1, max_tokens=(3000-prompt_tokens))
    llm_response = llm("format this rental listing into a YAML list that includes each property, and the address, beds, baths and URL for each: \n{}".format(body))
    response = "Listings URL: {}\nRental Listings: {}".format(query, llm_response)
    return response

def rental_listing_providers(query):
    # Fake tool, returns a fixed list of rental listing providers
    # (BROKEN) Domain - One of Australia's leading property sites, offering a wide range of rental listings for apartments, houses, and more. It services Australia. URL format: https://www.domain.com.au/rent/?suburb=melbourne-vic-3000
    # (BROKEN) RealEstate - A popular property site in Australia, with a large selection of rental listings across the country. It services Australia. URL format: https://www.realestate.com.au/rent/in-coburg,+victoria/list-1
    providers = """
    The following is a list of rental listing providers and an example URL that shows the format of how to search their rental listing pages:
     - Rent - A popular rental listing site that offers a wide range of rental listings for apartments, houses, and more. It services Australia. URL format: https://www.rent.com.au/properties/footscray+3011?surrounding_suburbs=1
     - Homely - A rental listing site that offers rental listings for apartments, houses, and more. It services Australia. URL: https://www.homely.com.au/for-rent/pascoe-vale-vic-3044/real-estate
     - OneRoof - A lesser-known rental listing site that offers a wide range of rental listings for apartments, houses, and more. It services New Zealand. URL format: https://www.oneroof.co.nz/search/houses-for-rent/suburb_auckland-central-auckland-city-3095_page_1
     - Open2view - A rental listing site that offers rental listings for apartments, houses, and more. It services New Zealand. URL: https://www.nz.open2view.com/
     - SpareRoom - A lesser-known rental listing site that offers a wide range of rental listings for apartments, houses, and more. It services the UK. URL: https://www.spareroom.co.uk/flatshare/search.pl
     - Gumtree AU - A rental listing site that offers rental listings for apartments, houses, and more. It services Australia. URL: https://www.gumtree.com.au/s-real-estate/c9296
    """
    return providers