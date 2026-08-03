# Day 7 - Rewriting Day 4's Loop with Smolagents

Goal for today: take day4's hand-written agent loop and rebuild it using smolagents' `CodeAgent`, in way fewer lines. Sounded simple. Took way longer than it should have, but I learned more from the errors than I would have from it just working first try.

## The plan going in

Day4 had a manual `for i in range(5)` loop, hand-written JSON tool schemas, and manual message appending after every tool call. The whole point of smolagents was replacing all of that — schemas get auto-generated from a `@tool` decorator + docstring, and the loop is handled internally by `CodeAgent`.

## Everything that broke, in order

**`@Tool` vs `@tool`.** Copied the capital-T version by habit. Turns out `Tool` is a class meant for subclassing, not a decorator for a plain function. Lowercase `@tool` is the actual decorator.

**`client=Groq(...)` instead of `model=OpenAIServerModel(...)`.** I swapped in a raw Groq SDK client thinking it'd work the same way, and got `TypeError: CodeAgent.__init__() missing 1 required positional argument: 'model'`. Ran `help(CodeAgent.__init__)` instead of guessing, and it turned out `CodeAgent` specifically wants a `smolagents.models.Model` object — not any SDK client, but smolagents' own wrapper. `OpenAIServerModel` is that wrapper.

**`token=` instead of `api_key=`.** This one was sneaky. I passed `token=os.environ.get("GROQ_API_KEY")` and it didn't throw an error where I expected. Instead it failed two layers down with `openai.OpenAIError: Missing credentials`. Turns out `OpenAIServerModel` has no `token` parameter — it has `api_key`. Because the class also accepts `**kwargs`, my bad keyword didn't crash, it just got silently absorbed and ignored, so `api_key` stayed empty the whole time. Only found this by actually printing the real signature with `help()` instead of assuming I remembered it right.

**Wrong model name.** Used `meta-llama/Llama-3.3-70B-Instruct` (Hugging Face style) and got a 404 `model_not_found` from Groq. Groq wants its own short name — `llama-3.3-70b-versatile`, the same one I already had working in day4. Should've caught this immediately, didn't.

## The part that actually mattered

Once it finally ran clean, I noticed something: my `multiply` tool never got called. The agent just wrote `celsius * 3` directly in Python instead.

At first I thought "it still got the right answer, so who cares." But that's not actually the goal — day4's whole point was proving the model *has* to use a tool, it can't just do the math itself. So I tested it: reran the exact same prompt but added "use the multiply tool for the multiplication step" at the end. That time it called `multiply(a=celsius, b=3)` for real.

So the actual finding: in day4's loop, tool use wasn't optional — the model literally had no other way to multiply two numbers, that was the only path. In `CodeAgent`, tools are just extra functions sitting in scope. If the model can already do something in plain Python (like arithmetic), it'll skip your tool and do it inline — unless you explicitly tell it not to. Registering a tool doesn't mean it gets used.

## What I actually learned today

Getting the "right answer" isn't the same as proving what you set out to prove — I almost deleted the `multiply` tool entirely because it "wasn't being used," which would've quietly turned this into a different, weaker demo than what day4 was actually showing. Also: `help(Class.__init__)` beats guessing parameter names every time — two of today's bugs were exactly that, and one of them failed silently instead of loudly, which is worse.

## Next
- Retry logic for flaky model output — still carried over from day5/6, still not done.