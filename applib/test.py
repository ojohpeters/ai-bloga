import requests
import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv('API_KEY')
API_URL = getenv('API_URL')


prompt = '''

Write a professional blog post about the Nigeria Premier League (NPL) with a length of at least 400 words. The post should be formatted using proper Markdown for WordPress, including:

    # for main titles
    ## for subheadings
    Bullet points - for key points
    Numbered lists for rankings or steps
    Tables for statistics if relevant
    **bold text** for emphasis
    Inline links [text](URL) where applicable

Cover the following sections:

    Introduction - Overview of the NPL and its significance
    History and Growth - How the league has evolved
    Notable Teams and Players - Mention key clubs and stars who emerged from NPL
    Recent Developments - Changes like VAR, stadium upgrades, or sponsorships
    Challenges & Solutions - Financial struggles, viewership issues, and potential fixes
    Conclusion - Future prospects and why NPL is important to African football

Make sure the writing is engaging, professional, and SEO-friendly, including keywords like 'Nigeria Premier League', 'NPL teams', and 'African football'. Avoid fluff and ensure all data is accurate.

'''

print(API_KEY)
response = requests.post(
  url=API_URL,
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
   data=json.dumps({
    "model": "qwen/qwen2.5-vl-72b-instruct:free", # Optional
    "messages": [
      {"role": "user", "content": prompt}
    ],
    "top_p": 1,
    "temperature": 0.7,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "top_k": 0,
  })
)

print(response.content)