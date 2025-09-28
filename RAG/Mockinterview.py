from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

prompt = PromptTemplate(
    input_variables=["role", "jd"],
    template=""" You are a senior technical interviewer.
    Given the job role: {role}
    And the job description: {jd}
    
    Generate 5 **technical interview questions** that are relevant to the job role and description.
    Only include questions that test technical skills and knowledge or problem-solving abilities.
    Do NOT include situational or behavioral questions.

    For each questio with clear and strong sample answer.
    1. Question 1: .....
    2. Question 2: .....
    """
)
chain = LLMChain(llm=llm, prompt=prompt)

st.title("Mock Interview Question Generator!")
role = st.text_input("Enter the Job Role:")
jd = st.text_area("Enter the Job Description:")

if st.button("Generate Q&A"):
    if role.strip() == "" or jd.strip() == "":
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating interview questions..."):
            response = chain.invoke({"role": role, "jd": jd})
        st.subheader("Moke Interview Questions:")
        st.write(response)
