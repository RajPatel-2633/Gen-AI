import os
import json
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key= os.environ.get("GROQ_API_KEY")
)

def get_weather(city):
    # Return the temperature of city
    print("Tool called get_weather with city",city)

    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

available_tools = {
    "get_weather":{
        "fn":get_weather,
        "description":"Takes a city name as input and returns the current weather for the city"
    }
}

system_prompt = f'''
  You are an helpful AI Assistant who is specialised in resolving user query.
  You work on start, plan,action, observe mode.
  For the given user query and available tools, plan the step by step execution, based on the planning.
  Select the relevant tool from the available tool.And based on the tool selection you perform an action to call the tool.
  Wait for the observation and based on the observation from the tool call resolve the user query.

  Rules:
  -Follow the Output JSON Format.
  -Always perform one step at a time and wait for the next input.
  -Carefully analyze the user query

  Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

  Available Tools:
  - get_weather: Takes a city name as an input and returns the current weather for the city

  Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

'''

messages=[
    {"role":"system","content":system_prompt}
]

user_query = input("> ")

messages.append({"role":"user","content":user_query})

while True:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_output = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsed_output)})

    if  parsed_output.get("step") == "plan":  #parsed_output is an object so we can apply .get and inside it we can write its key
        print(f"{parsed_output.get('content')}")
        continue

    if  parsed_output.get("step") == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if available_tools.get(tool_name,False)!=False:
            output = available_tools[tool_name].get("fn")(tool_input)  # This is a function  call ( Ek baar me ek hi tool ayega) There can be many tools
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            continue

    if  parsed_output.get("step") == "output":
        print(f"{parsed_output.get('content')}")
        break
