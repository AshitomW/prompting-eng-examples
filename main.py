from fastapi import FastAPI, Body
from ollama import Client 



app = FastAPI()
client = Client(
  host="http://localhost:11434",
)


@app.post("/chat")
def chat(message:str = Body(...,description="The message")):
  response = client.chat(model="gemma3:1b", messages=[
    {"role":"user","content":message}
  ])

  return {"response":response.message.content}

