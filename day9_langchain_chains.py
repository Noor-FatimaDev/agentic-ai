from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

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