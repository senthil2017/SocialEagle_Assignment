import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🌈 Kids Chat Bot 🤖",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for colorful, kid-friendly design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        font-size: 16px;
        font-weight: 500;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px 0 rgba(252, 182, 159, 0.4);
        font-size: 16px;
        font-weight: 500;
    }
    
    .title-container {
        text-align: center;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
    
    .fun-button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 15px 0 rgba(240, 147, 251, 0.4);
        transition: all 0.3s ease;
    }
    
    .fun-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(240, 147, 251, 0.6);
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 10px 20px;
        font-size: 16px;
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    .bounce {
        animation: bounce 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:3000/api/v1/prediction/c4b4d1f1-602e-4dc5-a540-e535778d21f0"

def query_api(question):
    """Query the API with a question"""
    try:
        payload = {"question": question}
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "🔌 Oops! I can't connect to the chat bot right now. Make sure the server is running!"}
    except requests.exceptions.Timeout:
        return {"error": "⏰ The chat bot is thinking too hard! Try asking something else."}
    except requests.exceptions.RequestException as e:
        return {"error": f"🤖 Something went wrong: {str(e)}"}
    except Exception as e:
        return {"error": f"😅 Unexpected error: {str(e)}"}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bot_name" not in st.session_state:
    st.session_state.bot_name = "Buddy"

# Main title with emojis
st.markdown("""
<div class="title-container">
    <h1>🌈 Welcome to the Magical Chat Bot! 🤖</h1>
    <h3>Ask me anything and let's have fun together! 🎉</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar with fun options
with st.sidebar:
    st.header("🎨 Fun Settings")
    bot_name = st.text_input("🤖 What should I call your bot?", value=st.session_state.bot_name)
    if bot_name != st.session_state.bot_name:
        st.session_state.bot_name = bot_name
    
    st.header("🎯 Quick Questions")
    quick_questions = [
        "🌟 Tell me a fun fact!",
        "🦄 What's your favorite color?",
        "🎈 Can you tell me a joke?",
        "🌍 What's the coolest animal?",
        "🚀 Tell me about space!",
        "🎵 Do you like music?"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}"):
            # Process quick question immediately
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Query the API for quick questions
            with st.spinner(f"🤖 {st.session_state.bot_name} is thinking..."):
                response = query_api(question)
                
                if "error" in response:
                    bot_response = response["error"]
                else:
                    if isinstance(response, dict):
                        bot_response = response.get("text", response.get("answer", response.get("response", str(response))))
                    else:
                        bot_response = str(response)
            
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            st.rerun()

# Main chat area
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'''
            <div class="user-message">
                <strong>🧒 You:</strong> {message["content"]}
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="bot-message">
                <strong>🤖 {st.session_state.bot_name}:</strong> {message["content"]}
            </div>
            ''', unsafe_allow_html=True)
    
    # Chat input with form to handle Enter key
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "💬 Type your message here:",
            placeholder="Ask me anything! 🌟",
            key="user_input_form",
            label_visibility="collapsed"
        )
        
        # Send button with custom styling
        col_send1, col_send2, col_send3 = st.columns([2, 1, 2])
        with col_send2:
            send_button = st.form_submit_button("🚀 Send!", use_container_width=True)
    
    # Process user input
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show loading animation
        with st.spinner(f"🤖 {st.session_state.bot_name} is thinking..."):
            # Query the API
            response = query_api(user_input)
            
            # Add bot response
            if "error" in response:
                bot_response = response["error"]
            else:
                # Extract the response text (adjust based on your API response structure)
                if isinstance(response, dict):
                    bot_response = response.get("text", response.get("answer", response.get("response", str(response))))
                else:
                    bot_response = str(response)
        
        st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        # Clear any remaining text in session state
        if "user_input_form" in st.session_state:
            del st.session_state["user_input_form"]
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fun facts section
with st.expander("🌟 Fun Features"):
    st.write("""
    🎨 **Colorful Design**: Enjoy beautiful gradients and animations!
    
    🤖 **Custom Bot Name**: Give your chat bot a special name!
    
    ⚡ **Quick Questions**: Click the buttons in the sidebar for instant fun!
    
    💾 **Chat History**: Your conversation stays until you clear it!
    
    🔄 **Real-time Responses**: Get instant answers from your API!
    """)

# Instructions for parents/teachers
with st.expander("👨‍👩‍👧‍👦 For Parents & Teachers"):
    st.write("""
    This chat application connects to a local API for safe, controlled interactions:
    
    🔧 **Setup**: Make sure your API server is running on `localhost:3000`
    
    🛡️ **Safety**: All conversations go through your local server
    
    🎯 **Educational**: Great for learning about technology and communication
    
    ⚙️ **Customizable**: Modify the quick questions to match learning objectives
    """)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 50px; padding: 20px;'>
    <p style='color: #666; font-size: 14px;'>
        Made with ❤️ for curious kids everywhere! 🌈✨
    </p>
</div>
""", unsafe_allow_html=True)