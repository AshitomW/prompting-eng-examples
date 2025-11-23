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


# Zero Shot Prompting : Directly Giving The Instructions To The Model
# Model is given direct question or task without any prior example.
SYSTEM_PROMPT = "You should only answer coding related questions. Do not answer anything else. Any Questions other than coding should be discarded and just say sorry."


response = client.chat.completions.create(
  model="gemini-2.5-flash",
  messages=[
    {"role":"system","content":SYSTEM_PROMPT},
    {"role":"user","content":"Hey, can you code a program that prints hello"}
    
  ]
)

print(response.choices[0].message.content)