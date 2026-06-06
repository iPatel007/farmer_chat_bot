from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

import os

# Try to get API key from multiple sources
api_key = None

# Method 1: Try Streamlit Cloud Secrets
try:
    import streamlit as st
    if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
        api_key = st.secrets['OPENAI_API_KEY']
        print("✅ Using API key from Streamlit secrets")
except (ImportError, AttributeError):
    pass

# Method 2: Fallback to environment variable (local development)
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ Using API key from environment variable")

# Method 3: Show clear error if no API key found
if not api_key:
    raise ValueError(
        "❌ OPENAI_API_KEY not found!\n"
        "For Streamlit Cloud: Add OPENAI_API_KEY in Secrets (Settings → Secrets)\n"
        "For local development: Create .env file with OPENAI_API_KEY=your_key"
    )

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

# Initialize Embedding Model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)