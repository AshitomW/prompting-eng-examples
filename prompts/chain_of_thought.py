from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_KEY")
API_URL = os.getenv("GEMINI_URL")

client = OpenAI(
  api_key=API_KEY,
  base_url=API_URL
)


SYSTEM_PROMPT = """
  You're an expert AI Assistant in resolving user queries using chain of thought.
  You work on START, PLAN and OUTPUT Steps.
  You need to first PLAN what needs to be done. The plan can be multiple steps.
  Once you think enough plan has been done, finally you can give an OUTPUT.


  Rules: 

  - Strictly Follow the given JSON output format
  - Only run one step at a time
  - The sequence of steps is START (where user gives an input) , PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user.)


  Output Format: 

  {{
    "step":"start" | "plan" | "output",
    "content":"string"
  }}


  Examples:

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


  
  

"""


print("\n\n\n")

message_history = [
  {"role":"system","content":SYSTEM_PROMPT}
]


query = input(">> ")
message_history.append({"role":"user","content":query})


while True:
  response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"}, 
    messages=message_history
  )

  raw_response = response.choices[0].message.content
  message_history.append({"role":"assistant","content":raw_response})
  parsed_result = json.loads(raw_response)
  if parsed_result.get("step") == "START":
    print("Starting....",parsed_result.get("content"))
    continue
  
  if parsed_result.get("step") == "PLAN":
    print("Thinking...\n", parsed_result.get("content"))
    continue 

  if parsed_result.get("step") == "OUTPUT":
    print("Output:\n", parsed_result.get("content"))
    break



# response = client.chat.completions.create(
#   model="gemini-2.5-flash",
#   response_format={"type":"json_object"},
#   messages=[
#     {"role":"system","content":SYSTEM_PROMPT},
#     {"role":"user","content":"Hey, write a code to add n numbers in js"},

#   ]
# )

# print(response.choices[0].message.content)


print("\n\n\n")