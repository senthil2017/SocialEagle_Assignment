import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4o",temperature=0.2)

embeddings = OpenAIEmbeddings()

st.title("RAG with Streamlit and LangChain")

upload_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if upload_file is not None:
    raw_text=""

    try:
        pdf_reader = PdfReader(upload_file)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    except Exception as e:
        st.error(f"Error reading PDF file: {e}")

    if not raw_text.strip():
        st.error("No text found in the uploaded PDF.")
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(raw_text)

        if not texts:
            st.error("Text splitting resulted in no chunks.")
        else:
            st.success(f"Text split into {len(texts)} chunks.")

            vectorstore = FAISS.from_texts(texts, embeddings)

            retriever = vectorstore.as_retriever()

            system_prompt = (
                            "You are an assistant for question-answering tasks. "
                            "Use the following pieces of retrieved context to answer "
                            "the question. If you don't know the answer, say that you "
                            "don't know. Use three sentences maximum and keep the "
                            "answer concise."
                            "\n\n"
                            "{context}"
                        )

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            #qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriver=vectorstore.as_retriever)

            query=st.text_input("Ask a question about the document:")

            doc_chain = create_stuff_documents_chain(llm,prompt)
            qa = create_retrieval_chain(retriever,doc_chain)
            if query:
                with st.spinner("Generating answer..."):
                    try:
                        response = qa.invoke({"input": query})
                        st.subheader("Answer")
                        st.write(response["answer"])
                    except Exception as e:
                        st.error(f"Error generating answer: {e}")
print("RAG/Rag_app.py loaded")
