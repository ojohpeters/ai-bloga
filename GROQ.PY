import os

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("API_KEY2"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is the latest sport new for today ",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)