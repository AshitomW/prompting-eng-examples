from openai import OpenAI
from dotenv import load_dotenv
import os 
import requests 
from pydantic import BaseModel, Field
from typing import Optional
import json

# client = Client(
#   host="http://localhost:11434"
# ) 


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_API_URL = os.getenv("GEMINI_URL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
client = OpenAI(
  api_key=GEMINI_API_KEY,
  base_url=GEMINI_API_URL
)





# Pretrained thing , cannot have the real time data.
# We need some kind of api to get real time data.
def main_base():
  user_query = input("> ")
  response = client.chat.completions.create(
    model=GEMINI_MODEL,
    messages=[
      {"role":"user","content":user_query}
    ]
  )

  print(f"🤖: {response.choices[0].message.content}")



def get_weather(city: str):
  url = f"https://wttr.in/{city}?format=%C+%t"
  response = requests.get(url=url)
  if response.status_code == 200: 
    return f"The weather in {city} is  {response.text}"
  return "Something Went Wrong"


# allow the model to run the get weather api call.

# chain of thoughts



class OutputFormat(BaseModel):
  step: str = Field(...,description="The ID Of the step. Example : It Can be PLAN,OUTPUT, TOOL, etc.")
  content: Optional[str] = Field(None,description="The optional string content for the step")
  tool: Optional[str] = Field(None, description="The ID of the tool to call.")
  input: Optional[str] = Field(None, description="The input parameter of the tool to call.")





SYSTEM_PROMPT = """
You are an agent that must output EXACTLY ONE step per response.

You NEVER jump directly to OUTPUT.  
You MUST always reply with only one of the steps below:

- "START" (only when reacting to the user's initial query)
- "PLAN" (your internal reasoning steps; may occur many times)
- "TOOL" (when you must call a tool)
- "OUTPUT" (only after all planning and tool calls are done)

CRITICAL RULES:
1. Respond with ONLY ONE JSON OBJECT per turn.
2. NEVER skip steps. You MUST produce at least one PLAN before OUTPUT.
3. NEVER include START except as the very first response.
4. TOOL steps MUST contain:
   {
     "step":"TOOL",
     "tool":"get_weather",
     "input":"Kathmandu"
   }
5. AFTER a TOOL call, you must WAIT for OBSERVE input.
   You do NOT produce OUTPUT immediately.

When you receive OBSERVE, you must continue with PLAN steps.

JSON Format (MANDATORY):
{
  "step":"START" | "PLAN" | "TOOL" | "OUTPUT",
  "content":"string",
  "tool":"string (optional)",
  "input":"string (optional)"
}



  Example_1:

  START: Hey , can you solve 2 + 3 *4 / 10
  PLAN: {"step":"PLAN", "content":"Seems like user is interested in maths problem"},
  PLAN: {"step:"PLAN","content":"Looking at the problem, we shodl solve this using the BODMAS method"},
  PLAN: {"step":"PLAN", "content":"Yes, the bodmas method is appropriate rule for this expression"},
  PLAN: {"step":"PLAN", "content":"First we should multiply 3 and 4 which is 12"},
  PLAN: {"step":"PLAN", "content":"Now the new equation is 2 + 12 / 10"},
  PLAN: {"step":"PLAN", "content":"Now we should perform division on 12 / 10 which results in 1.2"},
  PLAN: {"step":"PLAN", "content":"Now the resulting equation is 2 + 1.2"},
  PLAN: {"step":"PLAN", "content":"Now performing  addtion of 2 + 1.2 we get 3.2"},
  PLAN: {"step":"PLAN", "content":"since there are no more operations to be done , the final result is 3.2"},
  OUTPUT: {"step":"OUTPUT", "content":"2 + 3 * 4 / 10 = 3.2 "},

  Example_Two:

  START: What is the current real-time weather of kathmandu?
  PLAN: {"step":"PLAN", "content":"Seems like user is interested in getting weather of Kathmandu , Nepal"},
  PLAN: {"step:"PLAN","content":"Let's see if we have any tool from the list of available tools"},
  PLAN: {"step":"PLAN", "content":"Great, we have get_weather(city:str) tool available for this query."},
  PLAN: {"step":"PLAN", "content":"I need to call get_weather tool with kathmandu as input argument for the city parameter"},
  PLAN: {"step":"TOOL", "tool":"get_weather", "input":"Kathmandu"},
  PLAN: {"step":"OBSERVE","tool":"get_weather", "content":"The temperature of kathmandu is misty with 9 degree celcius"},
  PLAN: {"step":"PLAN", "content":"Great, I got the weather details about kathmandu"},
  OUTPUT: {"step":"OUTPUT", "The current weather in kathmandu is about 9 degree celcius with misty atmosphere"},  
  

"""





def main_agent():
  message_history = [
    {"role":"system","content":SYSTEM_PROMPT}
  ]

  query = input(">> ")
  message_history.append({"role":"user","content":query})
  available_tools = {
    "get_weather": get_weather
  }

  while True:
    response = client.chat.completions.parse(
      model=GEMINI_MODEL,
      response_format=OutputFormat,
      messages=message_history
    )

    raw_response = response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_response})
    parsed_result = response.choices[0].message.parsed
    
    if parsed_result.step == "START":
      print("Starting....",parsed_result.content)
      continue 
    
    if parsed_result.step == "PLAN":
      print("Thinking...\n",parsed_result.content)
      continue 
    
    if parsed_result.step == "OUTPUT":
      print("Ouput:\n",parsed_result.content)
      break 
    
    if parsed_result.step == "TOOL":
      tool = parsed_result.tool
      tool_input = parsed_result.input
      print(f"Tool: {tool} with input: {tool_input}")
      tool_response = available_tools[tool](tool_input)
      message_history.append({"role":"developer","content":json.dumps(
        {"STEP":"OBSERVE","tool":tool, "input":tool_input, "output": tool_response }
       )})
      continue

  


main_agent()