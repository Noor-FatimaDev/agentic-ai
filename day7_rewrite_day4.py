from smolagents import OpenAIServerModel, tool, CodeAgent
from dotenv import load_dotenv
import os
load_dotenv()
model = OpenAIServerModel(model_id="llama-3.3-70b-versatile", api_key=os.environ.get("GROQ_API_KEY"), api_base=os.environ.get("GROQ_API_BASE"))
@tool
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers together.
    Args:
        a: The first number.
        b: The second number.
    """
    return a * b
agent = CodeAgent(tools=[multiply], model=model, add_base_tools=True)
agent.run(
    "What's the temperature in Lahore in celsius, and what is that multiplied by 3? use the multiply tool for the multiplication step.",
)
