# imports
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2:1b"

# Create a messages list using the same format that we used for OpenAI
messages = [
    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
]

payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

# Let's just make sure the model is loaded
# !ollama pull llama3.2:1b
response = ollama.chat(model=MODEL, messages=messages)
print(response['message']['content'])
