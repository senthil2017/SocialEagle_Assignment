#from langchain_community import OpenAI, LLMChain, PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7)

prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""You are a helpful assistant that helps people find information.
Given the user input, provide a concise and relevant response.
User Input: {user_input}
Your Response: """)

chain = LLMChain(llm=llm, prompt=prompt)

if __name__ == "__main__":
    user_input = input("Enter your query:")
    response = chain.run(user_input)
    print("AI Says:", response)