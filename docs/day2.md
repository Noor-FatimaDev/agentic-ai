# Day 2 — Prompting Fundamentals

Today was about understanding how the way you phrase a prompt changes what the model does. I tested three core prompting techniques: zero-shot, few-shot, and chain-of-thought — all using raw API calls, no framework.

## What I built

A single script with a reusable `ask(prompt)` function that sends any prompt to the Groq API and returns the response text. Called it three times with three different prompting styles and compared the outputs directly.

```python
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 1. Zero-shot
zero_shot_prompt = "Classify this review as positive or negative: 'The food was cold and the service was slow.'"

# 2. Few-shot
few_shot_prompt = """
Review: 'Amazing food, loved it!' -> Positive
Review: 'Terrible experience, never coming back' -> Negative
Review: 'The food was cold and the service was slow.' ->
Reply with only one word: Positive or Negative.
"""

# 3. Chain-of-thought
cot_prompt = "A store had 23 apples, sold 8, then got a delivery of 15 more. How many apples now? Think step by step before giving the final answer."

print("----- ZERO-SHOT -----")
print(ask(zero_shot_prompt))

print("\n----- FEW-SHOT -----")
print(ask(few_shot_prompt))

print("\n----- CHAIN-OF-THOUGHT -----")
print(ask(cot_prompt))
```

The `ask()` function exists so I don't repeat the same API call block three times — wrap repeated logic in a function, call it with different inputs.

## The three techniques and what I actually observed

**Zero-shot** — just ask, no examples. The model answered correctly but was verbose, added its own unsolicited reasoning, and in an earlier run actually hallucinated a fact that wasn't in the prompt at all ("the dessert was good" — there was no dessert mentioned). It invented it confidently. This is called hallucination and it's a real problem in agents because a hallucinated tool input or fact can silently break a pipeline.

**Few-shot** — give examples first to show the pattern you want. First run the model still added explanation after "Negative." Added one line to the prompt: *"Reply with only one word: Positive or Negative."* Second run came back as just "Negative." — nothing else. This is output format control: telling the model exactly what shape the answer should be. Critical for agents because they need to parse LLM output programmatically — you can't parse a paragraph when you expected a single word.

**Chain-of-thought** — ask the model to reason step by step before answering. It broke the apple problem into 3 clear steps, showed the math at each step, then gave the final answer. No hallucination because every step was grounded in numbers I gave it. This is the "Reason" part of the ReAct agent loop — agents use chain-of-thought internally to decide what action to take next before actually taking it.

## Key takeaway

Small prompt changes produce big behavioral changes. Zero-shot, few-shot, and chain-of-thought aren't just academic categories — they map directly to how you'll prompt agents to reason, format their output, and avoid making things up.

## Next

Day 3 — function calling: how an LLM decides to call a tool instead of just answering in text.