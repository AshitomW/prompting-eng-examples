from openai import OpenAI
from dotenv import load_dotenv
import os 
load_dotenv()

API_KEY = os.getenv("GEMINI_KEY")
API_URL = os.getenv("GEMINI_URL")

client = OpenAI(
  api_key=API_KEY,
  base_url=API_URL
)


response = client.chat.completions.create(
  model="gemini-2.5-flash",
  messages=[
    {"role":"user","content":"Hey There"}
  ]
)

print(response.choices[0].message)