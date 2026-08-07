import os
from dotenv import load_dotenv

load_dotenv()

print("API KEY:", os.getenv("LANGCHAIN_API_KEY"))
print("PROJECT:", os.getenv("LANGCHAIN_PROJECT"))
print("TRACING:", os.getenv("LANGCHAIN_TRACING_V2"))