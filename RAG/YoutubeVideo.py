from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""You are an expert summarizer.
        Here is a video transcript: 
        {transcript}

        Please provide a concise summary of the key points discussed in the video. Make sure the summary is clear and easy to understand.""",
)

chain = LLMChain(llm=llm, prompt=summary_prompt)

st.title("YouTube Video Summarizer")

video_url = st.text_input("Enter YouTube Video URL:")

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""

    parse_url = urlparse(url)
    if parse_url.hostname == 'youtu.be':
        return parse_url.path[1:]
    elif parse_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parse_url.query)
        return query.get('v', [None])[0]
    return None

if st.button("Generate Summary"):
    if video_url.strip() == "":
        st.error("Please enter a YouTube video URL.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
        else:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                transcript = " ".join([item['text'] for item in transcript_list])

                summary = chain.invoke({"transcript": transcript})

                st.subheader("Video Summary:")
                st.write(summary)

            except Exception as e:
                st.error(f"Error fetching transcript: {e}")


            
 