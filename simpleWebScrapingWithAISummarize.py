import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import anthropic
from IPython.display import display, Markdown

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('ANTHROPIC_API_KEY')

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        
        # Remove irrelevant elements
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = "No body content found"

# System prompt for Claude
system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "user", "content": f"{system_prompt}\n\n{user_prompt_for(website)}"}
    ]

def summarize(url):
    website = Website(url)
    
    # Create the message using Anthropic's format
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Using Claude 3 Haiku for cost efficiency
        max_tokens=1024,
        messages=messages_for(website)
    )
    
    # Extract content from Anthropic's response format
    return response.content[0].text

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# Test the functionality
if __name__ == "__main__":
    # Test website creation
    url = "https://anthropic.com"
    wa = Website(url)
    print(f"Title: {wa.title}")
    print(f"Text preview: {wa.text[:200]}...")
    
    # Test summarization
    display_summary(url)
