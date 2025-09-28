from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st
import PyPDF2

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

letter_prompt = PromptTemplate(
    input_variables=["resume_text", "job_title", "company_name"],
    template="""You are a professional cover letter writer. Using the following resume text and job details, write a concise and compelling cover letter:
   
    Job Title: {job_title}
    Company Name: {company_name}

    Use the following resume formation:
    {resume_text}
    Provide a clear, well-structured cover letter that highlights relevant skills and experiences.""")

chain = LLMChain(llm=llm, prompt=letter_prompt)

st.title("Cover Letter Generator!")

upload_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_title = st.text_input("Enter the Job Title:")
company_name = st.text_input("Enter the Company Name:")

if st.button("Generate Cover Letter"):
    if not upload_file or job_title.strip() == "" or company_name.strip() == "":
        st.error("Please upload a resume and fill in all fields.")
    else:
        try:
            pdf_reader = PyPDF2.PdfReader(upload_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            resume_text = ""

        if not resume_text.strip():
            st.error("No text found in the uploaded PDF.")
        else:
            with st.spinner("Generating cover letter..."):
                response = chain.invoke({
                    "resume_text": resume_text,
                    "job_title": job_title,
                    "company_name": company_name
                })
            st.subheader("Generated Cover Letter:")
            st.write(response)