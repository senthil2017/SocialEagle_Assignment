import streamlit as st

# App Title with emoji
st.title("👋 Welcome to the Greeting App!")

# Input fields
name = st.text_input("🧑 What's your name?", "John")
age = st.slider("🎂 Select your age:", min_value=1, max_value=100, value=25)

# Submit button with emoji
if st.button("🚀 Submit"):
    if name:
        st.success(f"👋 Hello, {name}! You are {age} years old.")
    else:
        st.warning("Please enter your name to get a greeting.")
