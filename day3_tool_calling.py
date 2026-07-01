from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def multiply(a, b):
    return a * b

def get_weather(city):
    return f"The weather in {city} is sunny with a temperature of 30°C."

tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiplies two numbers together and returns the result",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetches the weather information for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to fetch weather for"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What's the weather in Lahore and what is 10 multiplied by 5?"}
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

print("--- STEP 1: Model's first response ---")
print("finish_reason:", response.choices[0].finish_reason)
print("tool_calls:", response.choices[0].message.tool_calls)

if response.choices[0].finish_reason == "tool_calls":

    messages.append(response.choices[0].message)

    print("\n--- STEP 2: Executing all tools ---")

    # loop runs all tools, appends all results — no API call inside here
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "multiply":
            result = multiply(arguments["a"], arguments["b"])
        elif function_name == "get_weather":
            result = get_weather(arguments["city"])

        print(f"Ran {function_name} → result: {result}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

    # final API call happens ONCE after all tools have run
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools
    )

    print("\n--- STEP 3: Model's final answer ---")
    print(final_response.choices[0].message.content)
    print("finish_reason:", final_response.choices[0].finish_reason)