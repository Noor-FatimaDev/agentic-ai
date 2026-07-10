# Day 4 — Agent Loop

Today was about building the actual loop that makes an agent an agent. Not a single API call, not a one-shot if/else — a real repeating loop that keeps running until the task is fully done.

## What I built

A multi-step agent loop using a `for` loop with a `break` condition. The agent keeps calling the LLM, checks if it needs to run a tool, runs it, feeds the result back, and repeats — until `finish_reason` is `stop`.

```python
available_functions = {"multiply": multiply, "get_weather": get_weather}

for i in range(5):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools
    )
    message = response.choices[0].message

    if response.choices[0].finish_reason != "tool_calls":
        print("Final answer:", message.content)
        break

    messages.append(message)
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = available_functions[call.function.name](**args)
        messages.append({
            "role": "tool", "tool_call_id": call.id,
            "name": call.function.name, "content": str(result)
        })
```

## What I observed

The question was: *"What's the temperature in Lahore, and what is that multiplied by 3?"*

The agent ran 3 iterations:
- **Iteration 1** — `finish_reason: tool_calls` → called `get_weather("Lahore")` → got `30°C`
- **Iteration 2** — `finish_reason: tool_calls` → called `multiply(30, 3)` → got `90`
- **Iteration 3** — `finish_reason: stop` → Final answer: `"The temperature in Lahore is 30°C and when multiplied by 3, the result is 90."`

The model used the weather result (30°C) as the input to `multiply` on its own — I never told it to chain those two steps. It reasoned across iterations autonomously. That's what makes this an agent and not just a function caller.

## Day 3 vs Day 4 — the real difference

In Day 3, the structure was a single `if` block with the final API call inside the tool loop. It could handle tools but only in one pass — if the task needed multiple steps it would break or give incomplete answers.

The `for` loop fixes this. The agent now:
1. Calls the LLM
2. Checks `finish_reason`
3. If `tool_calls` — runs the tool, appends result, loops again
4. If `stop` — breaks and returns the final answer

The loop is capped at 5 iterations (`range(5)`) to prevent infinite loops if something goes wrong — a safety pattern used in real production agents.

## `available_functions` — why it's cleaner than if/elif

Day 3 used this:
```python
if function_name == "multiply":
    result = multiply(...)
elif function_name == "get_weather":
    result = get_weather(...)
```

Day 4 replaces it with:
```python
available_functions = {"multiply": multiply, "get_weather": get_weather}
result = available_functions[call.function.name](**args)
```

One line instead of a growing if/elif chain. When you add a new tool, you just add it to the dictionary — the rest of the code doesn't change. This scales cleanly as agents grow to 10, 20, 50 tools.

## Next

Day 5 — system prompts: what they are, where they sit in the messages list, and how they control agent behavior across an entire conversation. Also finally fixing the hallucination from Day 3.