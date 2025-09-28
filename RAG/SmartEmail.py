from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

prompt = PromptTemplate(
    input_variables=["email_task"],
    template="""You are a professional email assistant. Helps the user to write email:
    {email_task}
    Provide clear and well explained email content with context."""
)

chain = LLMChain(llm=llm, prompt=prompt)

st.title("Smart Email Assistant using LLM")

st.write("Enter a key points for your email below:")

email_task = st.text_area("Points:", height=200)

if st.button("Generate Email"):
    if email_task.strip() == "":
        st.error("Please enter key points for the email.")
    else:
        with st.spinner("Generating email..."):
            response = chain.invoke({"email_task":email_task})
        st.subheader("Generated Email:")
        st.write(response)