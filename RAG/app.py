import streamlit as st
import PyPDF2
from io import StringIO
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage
import os
from datetime import datetime
import re

# Configure the page
st.set_page_config(
    page_title="AI Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #667eea;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(docx_file):
    """Extract text from uploaded DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def extract_text_from_txt(txt_file):
    """Extract text from uploaded TXT file"""
    try:
        stringio = StringIO(txt_file.getvalue().decode("utf-8"))
        text = stringio.read()
        return text
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return None

def clean_resume_text(text):
    """Clean and preprocess resume text"""
    # Remove extra whitespaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s.,;:()@-]', '', text)
    return text.strip()

def create_cover_letter_prompt():
    """Create the prompt template for cover letter generation"""
    template = """
    You are a professional career counselor and expert cover letter writer. Based on the provided resume, job role, and company information, create a compelling, personalized cover letter.

    Resume Content:
    {resume_text}

    Job Role: {job_role}
    Company Name: {company_name}
    Additional Details: {additional_info}

    Instructions:
    1. Write a professional cover letter that highlights relevant skills and experiences from the resume
    2. Tailor the content specifically for the job role and company
    3. Use a professional yet engaging tone
    4. Structure the letter with proper formatting (header, salutation, 3-4 body paragraphs, closing)
    5. Highlight 2-3 key achievements or skills that directly relate to the job role
    6. Show enthusiasm for the company and position
    7. Include a strong call to action
    8. Keep it concise (approximately 300-400 words)

    Generate a well-structured cover letter:
    """
    
    return PromptTemplate(
        input_variables=["resume_text", "job_role", "company_name", "additional_info"],
        template=template
    )

def initialize_llm():
    """Initialize the language model"""
    try:
        # You can replace this with other LLM providers like Anthropic, Cohere, etc.
        # For this example, we'll use OpenAI
        api_key = st.session_state.get('openai_api_key', '')
        if not api_key:
            return None
        
        llm = OpenAI(
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=api_key
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing LLM: {str(e)}")
        return None

def generate_cover_letter(resume_text, job_role, company_name, additional_info="", api_key=""):
    """Generate cover letter using LangChain"""
    try:
        # Set the API key temporarily
        os.environ["OPENAI_API_KEY"] = api_key
        
        llm = OpenAI(temperature=0.7, max_tokens=1000)
        prompt = create_cover_letter_prompt()
        chain = LLMChain(llm=llm, prompt=prompt)
        
        result = chain.run({
            "resume_text": resume_text,
            "job_role": job_role,
            "company_name": company_name,
            "additional_info": additional_info
        })
        
        return result
    except Exception as e:
        st.error(f"Error generating cover letter: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Cover Letter Generator</h1>
        <p>Create professional, tailored cover letters in minutes using AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to use the AI generation feature",
            placeholder="sk-..."
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### 📋 How to Use:
        1. Enter your OpenAI API key
        2. Upload your resume (PDF, DOCX, or TXT)
        3. Fill in job details
        4. Click 'Generate Cover Letter'
        5. Download your personalized cover letter
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 💡 Tips:
        - Ensure your resume is well-formatted
        - Be specific about the job role
        - Include company details for better personalization
        """)

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Resume Upload")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume in PDF, DOCX, or TXT format"
        )
        
        # Display file info
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text based on file type
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "text/plain":
                resume_text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file type")
                resume_text = None
            
            if resume_text:
                # Clean the text
                resume_text = clean_resume_text(resume_text)
                
                # Show preview
                with st.expander("📖 Resume Preview"):
                    st.text_area("Extracted Text", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200, disabled=True)
        else:
            resume_text = None
    
    with col2:
        st.header("💼 Job Details")
        
        # Job details form
        with st.form("job_details_form"):
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., Google, Microsoft, Apple",
                help="Enter the name of the company you're applying to"
            )
            
            job_role = st.text_input(
                "Job Role *",
                placeholder="e.g., Software Engineer, Data Scientist, Product Manager",
                help="Enter the specific job title or role"
            )
            
            additional_info = st.text_area(
                "Additional Information (Optional)",
                placeholder="Any specific requirements, company values, or details you'd like to highlight...",
                help="Add any additional context that might help personalize your cover letter",
                height=100
            )
            
            # Generate button
            generate_button = st.form_submit_button(
                "🚀 Generate Cover Letter",
                use_container_width=True
            )

    # Generation logic
    if generate_button:
        # Validation
        errors = []
        
        if not api_key:
            errors.append("Please enter your OpenAI API key in the sidebar")
        
        if not uploaded_file or not resume_text:
            errors.append("Please upload a valid resume file")
        
        if not company_name.strip():
            errors.append("Please enter the company name")
        
        if not job_role.strip():
            errors.append("Please enter the job role")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Show loading spinner
            with st.spinner("🤖 AI is crafting your perfect cover letter..."):
                cover_letter = generate_cover_letter(
                    resume_text=resume_text,
                    job_role=job_role,
                    company_name=company_name,
                    additional_info=additional_info,
                    api_key=api_key
                )
            
            if cover_letter:
                st.success("✅ Cover letter generated successfully!")
                
                # Display the generated cover letter
                st.header("📝 Your Generated Cover Letter")
                
                # Create two columns for display and download
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.text_area(
                        "Generated Cover Letter",
                        cover_letter,
                        height=400,
                        help="You can copy this text or download it as a file"
                    )
                
                with col2:
                    # Download button
                    st.download_button(
                        label="📥 Download as TXT",
                        data=cover_letter,
                        file_name=f"cover_letter_{company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                    
                    # Copy button (using JavaScript)
                    st.markdown("""
                    <button onclick="navigator.clipboard.writeText(document.querySelector('textarea[aria-label=\"Generated Cover Letter\"]').value)">
                        📋 Copy to Clipboard
                    </button>
                    """, unsafe_allow_html=True)
                
                # Success message
                st.markdown("""
                <div class="success-box">
                    <strong>🎉 Success!</strong> Your personalized cover letter has been generated. 
                    Review it carefully and make any necessary adjustments before sending.
                </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Built with ❤️ using Streamlit and LangChain</p>
        <p><strong>Note:</strong> Always review and personalize your cover letter before sending!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()