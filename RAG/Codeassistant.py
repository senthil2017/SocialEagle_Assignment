import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

prompt= PromptTemplate(
    input_variables=["user_input"],
    template="""You are professional coding assistant. Helps the user to write code:
    {code_task}
    Provride clear and well explained code with comments."""
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Code Assistant using LLM")

code_task = st.text_area("Describe your coding task:")

if st.button("Generate Code"):
    if code_task.strip() == "":
        st.error("Please enter a coding task description.")
    else:
        with st.spinner("Generating code..."):
            response = chain.invoke(code_task=code_task)
        st.subheader("Generated Code:")
        st.code(response, language="python")