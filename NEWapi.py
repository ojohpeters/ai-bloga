import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')
url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2025-02-17&'
       'sortBy=popularity&'
       f'apiKey={API_KEY}')

response = requests.get(url)

print(response.json())
print(API_KEY)