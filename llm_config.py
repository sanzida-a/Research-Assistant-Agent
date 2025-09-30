import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
GITHUB_EM_KEY = os.getenv("GITHUB_EM_KEY")


def get_llm(model="openai/gpt-4.1", temperature=0):
    """
    Returns a ChatOpenAI instance configured for GitHub Models API.
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=GITHUB_API_KEY,
        base_url="https://models.github.ai/inference/v1",
    )


def get_embeddings(model="openai/text-embedding-3-small"):
    """
    Returns an Embeddings instance configured for GitHub Models API.
    Note: GitHub Models uses a different base URL for embeddings.
    """
    return OpenAIEmbeddings(
        model=model,
        api_key=GITHUB_EM_KEY,
        base_url="https://models.github.ai/inference",
    )