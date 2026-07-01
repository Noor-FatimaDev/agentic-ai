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

# 1. Zero-shot — no examples given
zero_shot_prompt = "Classify this review as positive or negative: 'The food was cold and the service was slow.'"

# 2. Few-shot — examples given first to set the pattern
few_shot_prompt = """
Review: 'Amazing food, loved it!' -> Positive
Review: 'Terrible experience, never coming back' -> Negative
Review: 'The food was cold and the service was slow.' ->
Reply with only one word: Positive or Negative. 
"""

# 3. Chain-of-thought — ask it to reason step by step
cot_prompt = "A store had 23 apples, sold 8, then got a delivery of 15 more. How many apples now? Think step by step before giving the final answer."

print("----- ZERO-SHOT -----")
print(ask(zero_shot_prompt))

print("\n----- FEW-SHOT -----")
print(ask(few_shot_prompt))

print("\n----- CHAIN-OF-THOUGHT -----")
print(ask(cot_prompt))