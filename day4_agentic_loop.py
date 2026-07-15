from groq import Groq
from dotenv import load_dotenv
import os, json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def multiply(a, b):
    return a * b

def get_weather(city):
    return f"The weather in {city} is sunny with a temperature of 30°C."

available_functions = {"multiply": multiply, "get_weather": get_weather}

tools = [
    {"type": "function", "function": {
        "name": "multiply",
        "description": "Multiplies two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    }},
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "Fetches weather for a given city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }}
]

messages = [{"role": "system", "content": "Answer strictly using the tool results, without adding unstated details."},
        {"role": "user", "content": "What's the temperature in Lahore, and what is that multiplied by 3?"}]

for i in range(5):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools
    )
    message = response.choices[0].message
    print(f"\n--- Iteration {i+1} | finish_reason: {response.choices[0].finish_reason} ---")

    if response.choices[0].finish_reason != "tool_calls":
        print("Final answer:", message.content)
        break

    messages.append(message)
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = available_functions[call.function.name](**args)
        print(f"Ran {call.function.name}({args}) → {result}")
        messages.append({
            "role": "tool", "tool_call_id": call.id,
            "name": call.function.name, "content": str(result)
        })