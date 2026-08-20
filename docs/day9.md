# Day 9 LangChain Basics: Wrappers, Prompt Templates, Chains

## Goal
Understand and use LangChain's core building blocks: LLM wrappers, prompt templates, and chains the layer LangGraph itself is built on top of.

## What I built
A 2-step chain:
1. Topic -> YouTube channel name (via a prompt template + ChatGroq wrapper)
2. Channel name -> channel description (feeding step 1's output into step 2's template)

```python
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

name_prompt = ChatPromptTemplate.from_template("Suggest one YouTube channel name about {topic}.")
name_chain = name_prompt | llm
name_result = name_chain.invoke({"topic": "coding and drawing"})
channel_name = name_result.content

desc_prompt = ChatPromptTemplate.from_template("Write a short description for a YouTube channel called {channel_name}.")
desc_chain = desc_prompt | llm
desc_result = desc_chain.invoke({"channel_name": channel_name})

print(desc_result.content)
```

**Output:** Generated "CodeCanvas" as a channel name with a full matching description, chained end to end with no manual copy-pasting between steps.

## Concepts covered
- **LLM wrapper**: a standard interface (`ChatGroq`, etc.) so the rest of the code doesn't change if you swap providers.
- **Prompt template**: reusable text with `{slots}`, filled in per call instead of hand-writing f-strings each time.
- **Chain (`prompt | llm`)**: glues a template's output straight into the wrapper's input; `.invoke()` actually runs it.
- **`.content`**: `AIMessage` objects carry the reply text plus metadata; `.content` pulls just the text out, which matters when piping one chain's output into another chain's template slot.

## Bugs I hit and fixed (this was most of the day)
1. Double-wrapped constructor: `ChatGroq(ChatGroq(...))` instead of a single call.
2. Missing `load_dotenv()` — having a key in `.env` doesn't load it into Python automatically.
3. `model=` set to the string `"GROQ_API_KEY"` instead of an actual model name — confused the auth mechanism with the model selector.
4. Duplicated Groq base URL (`GROQ_API_BASE` already had `/openai/v1`, and the SDK appends it again) — fixed by trimming the env var to just the root domain.
5. Deprecated/unavailable model names (`mixtral-8x7b-32768`, `llama-3.3-70b-versatile`) — resolved by querying `client.models.list()` directly instead of guessing, landing on `openai/gpt-oss-20b`.

