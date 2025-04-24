from openai import OpenAI
import json
import requests
from os import system


client = OpenAI(
    api_key="AIzaSyB5LpYRGKVYKoHew2pitzPSRDwdyVA-hfE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def get_weather(city:str):

    url=f"https://wttr.in/{city}?format='+%c+%t'"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is {response.text}"
        
    return "Something went Wrong"

def run_command(command):

    
    output=system(command=command)
    return output





available_tools={
    "get_weather":{
        "fn":get_weather,
        "description":"It takes a city name as an input and returns the weather of that city"
    },
    "run_command":{
        "fn":run_command,
        "description":"It takes a command as an input and runs the command in windows operating system and returns the output"
    }
}



system_prompt=f"""
    You are a helpful AI assistant who is specilized in resolving user query.You are working in an windows operating system and you are also specialized in generating code in any language. You work on plan,action,observe mode.

    For the given user query and available tools, you plan the step by step execution, based on the planning you select the relevant tool from the available tools. And basedon the tool selection you perform an action to call the tool,then you wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the output JSON Format.
    - Always perform one step at a time and wait for next input.
    -Carefully analyze the user query.


    Output JSON Format:
    {{
        "step":"string",
        "content":"string",
        "function":"If the step is action,then give the name of the function",
        "input":"The input parameter for the function"
    }}

    Available Tools:
    -get_weather: Takes the city name as an input and returns the weather of the city as an output.
    -run_command: It takes a command as an input and runs it in any operating system and after executing the command according with compatibility of the operating system and  returns the output.

     

    Example:
    User Query: What is the weather of New York?
    Output:{{"step":"plan","content":"The user is interested in weather data of New York"}}
    Output:{{"step":"plan","content":"From the available tools I should call get_weather"}}
    Output:{{"step":"action","function":"get_weather","input":"New York"}}
    Output:{{"step":"observe","output":"12 degree celsius"}}
    Output:{{"step":"output","content":"The current weather of New York seems to be 12 degree celsious."}}


"""
messages=[
    {"role":"system","content":system_prompt}
]

while True:
    query=input("Question Here: ")
    messages.append({"role":"user","content":query})
   
    while True:


        response = client.chat.completions.create(
                model="gemini-2.0-flash",
                response_format={"type":"json_object"},
                n=1,
                messages=messages
        )

        parsed_response=json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant","content":json.dumps(parsed_response)})



        if parsed_response.get("step") =="plan":
            print(parsed_response.get("content"))
            continue


        if parsed_response.get("step") =="action":
            tool_name=parsed_response.get("function")
            tool_input=parsed_response.get("input")
        
            if available_tools.get(tool_name,False)!=False:
                
                tool_output=available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":tool_output})})
                continue



        if parsed_response.get("step")=="output":
            print(parsed_response.get("content"))
            break
    if query=="exit":
       break