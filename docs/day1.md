# Day 1 — First API call to an LLM

Today's goal was simple: make a raw API call to an LLM using Python, with no framework involved. Before touching LangChain or any agent library, I wanted to actually see what a request and response look like under the hood.

## Setup

Created a project folder with a virtual environment so dependencies stay isolated:

```
agentic-ai-journey/
├── docs
├── venv/
├── .env
└── day1_first_call.py
```

Installed two packages inside the venv:

```bash
pip install groq python-dotenv
```

- `groq` — official client to call Groq's API from Python
- `python-dotenv` — loads my API key from a `.env` file instead of hardcoding it in the script

`.env` just holds:
```
GROQ_API_KEY=my_key_here
```

## The script

```python
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Explain what an AI agent is in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
print(response)

```

`load_dotenv()` reads the `.env` file, `os.getenv()` pulls the key out of it, and that key is used to create a Groq client. The client sends the actual request through `chat.completions.create()`, and the answer comes back inside a response object — I print just the text part of it with `.choices[0].message.content`.

## What I learned from the full response object

I also printed the entire `response` object instead of just the text, to see the real structure:

- `message.role` — tells you who sent the message (`assistant` here). This is how conversation history gets tracked across turns.
- `finish_reason` — why the model stopped. `'stop'` means it finished normally. If it had wanted to call a function instead of answering, this would say `'tool_calls'` — that's the actual switch that controls agent behavior later on.
- `usage` — token counts for the input and output. This is what gets billed and rate-limited.
- `tool_calls` — was `None` this time, since I didn't give the model any tools yet.

The point of looking at this raw shape is that every agent framework I'll use later (LangChain, LangGraph, CrewAI) is just wrapping this exact request/response pattern with more logic on top. Seeing it bare on day one means none of it will feel like a black box later.

## Next

Day 2 — prompting fundamentals (zero-shot, few-shot, chain-of-thought) before building an agent loop from scratch.