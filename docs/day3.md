# Day 3 — Tool calling

Today was about understanding how an LLM decides to call a function instead of just answering in text. This is the core mechanical step that turns a plain LLM into an agent.

## What I built

A script with two tools — `multiply(a, b)` and `get_weather(city)` — both described to the model as JSON schemas. The model reads those descriptions, decides which tool to use based on the question, and requests the function call. My code then actually runs the function and sends the result back.

```python
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

    # append assistant message once, before the loop
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

    # final API call happens once after all tools have run
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools
    )

    print("\n--- STEP 3: Model's final answer ---")
    print(final_response.choices[0].message.content)
    print("finish_reason:", final_response.choices[0].finish_reason)
```

## How the loop actually works

The model never runs any code itself — it can only request that code be run. The flow is:

1. Send question + tool descriptions → model responds with `finish_reason: tool_calls` instead of `stop`, and populates the `tool_calls` field with the function name and arguments it wants
2. My code reads that request, runs the actual Python function, appends the result to messages with `role: tool`
3. Send the updated messages back → model reads the results and gives a final answer with `finish_reason: stop`

The important thing: `finish_reason` changes from `tool_calls` to `stop` only when the model has everything it needs and is done acting.

## Bug I ran into

First version had the final API call inside the `for` loop — so it fired after every single tool instead of once at the end. The fix was moving the final API call outside the loop but still inside the `if` block. In Python, indentation is structure — moving those lines one level left changed the entire execution order.

## Hallucination at output synthesis

My `get_weather` function returns a hardcoded `"30°C, sunny"`. The model received that exact string but synthesized it into `"28°C with a high, low, and slight chance of scattered showers"` — invented details that weren't in the data at all. This is hallucination happening at the output stage, not the input stage. In a real agent using live API data, this would mean mixing real and fabricated information in the same answer. The fix is a system prompt that constrains the model to only use data returned by tools — covered in Day 4.

## Why `json.loads()` matters

The model returns tool arguments as a JSON string, not a Python dictionary. Without `json.loads()` to convert it, trying to access `arguments["a"]` would fail silently or throw a type error. Always parse tool arguments before using them.

## Next

Day 4 — Agentic loop: The basic loop which is behind every agents working.