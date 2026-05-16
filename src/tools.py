import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_mistralai import ChatMistralAI

load_dotenv()

def get_tavily_client():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_mistral_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.1
    )

def search_company(company: str, context: str = "data AI consulting") -> str:
    client = get_tavily_client()
    results = client.search(
        query=f"{company} {context} services offering positioning",
        max_results=5
    )
    content = "\n\n".join([r["content"] for r in results["results"]])
    return content

def search_competitors(company: str, competitor: str) -> str:
    client = get_tavily_client()
    results = client.search(
        query=f"{competitor} vs {company} data AI consulting services",
        max_results=3
    )
    content = "\n\n".join([r["content"] for r in results["results"]])
    return content