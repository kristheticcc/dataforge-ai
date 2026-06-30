import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

# Setting up the client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)

# Model
model = "llama-3.3-70b-versatile"