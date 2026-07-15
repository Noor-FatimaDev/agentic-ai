# Day 6 — Fixing the Hallucination Bug + Doc Cleanup

No new features today. Just went back and actually fixed something I'd been putting off since Day 3 — the hallucination bug I mentioned "fixing next" twice in a row and never actually touched.

## The hallucination bug (finally fixed)

Quick recap of the bug: `get_weather()` just returns a hardcoded string — "The weather in Lahore is sunny with a temperature of 30°C." Nothing fancy. But when the model used that result to answer, it sometimes threw in extra stuff that was never in there — random things like "chance of showers" that it basically made up.

Before jumping to fix it I made myself think through why the lazy fixes wouldn't work:
- **temperature=0** — no, that just makes output more consistent run to run, it doesn't stop the model from confidently inventing details.
- **use a smarter model** — also no, a better model might hallucinate less in practice, but the actual problem (nothing telling it to stick to the tool output) is still there and could pop up again anytime.

What actually fixed it: adding a system message at the top of `messages` in both `day3_tool_calling.py` and `day4_agentic_loop.py`:

```python
{"role": "system", "content": "Answer strictly using the tool results, without adding unstated details."}
```

System prompt made sense as the spot for this since it sticks around for the whole conversation, even after the tool result comes back. It's a standing rule, not a one-time instruction.

## Then a random new error showed up

While testing the fix, `day4_agentic_loop.py` threw a `groq.BadRequestError` out of nowhere:

```
'failed_generation': '<function=get_weather{"city": "Lahore"}</function>'
```

First instinct was "great, I broke it with the system prompt." But instead of just assuming, I reran the exact same code with literally nothing changed — and it worked fine the second time.

Same code, same prompt, different result. So it wasn't the system prompt at all — the model just occasionally spits out a malformed tool call (some broken `<function=...>` tag instead of the format Groq actually expects), and the API rejects it because it can't parse it.

## What that actually means

Not a code bug, just the model being flaky sometimes. But it exposed a real gap — `day4_agentic_loop.py` has no error handling around the API call at all, so if this happens for real, the script just dies, even though trying again would've worked. Not fixing this today, just flagging it — it needs a `try/except` with retries before I'd trust it in anything real. And even then, retrying just papers over the flakiness, it doesn't actually stop the model from occasionally messing up the format.

## Doc cleanup

- README's progress table was stuck at Day 2 even though Day 3-5 code already existed. Fixed, now it lists all five.
- `day3.md` and `day4.md` both had the same leftover line about "fixing the hallucination next" that never actually happened. Fixed both to point here instead.

## What I actually learned today

"It broke" and "it broke once and now it's fine" are not the same problem, and I almost debugged the wrong one. If I hadn't reran it before touching more code, I probably would've gone down a rabbit hole blaming the system prompt for something it didn't cause. Also — letting docs go stale for two days straight is exactly how a real bug quietly disappears from the radar. Won't let that happen again.

## Next
- Actually read the ReAct paper — still owe myself this one.
- Add retry logic to `day4_agentic_loop.py` for the flaky tool-call formatting.