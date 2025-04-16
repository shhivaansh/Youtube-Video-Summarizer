import streamlit as st  # Streamlit for creating the web app interface
from dotenv import load_dotenv  # To load environment variables from a .env file
import os  # To access environment variables
import google.generativeai as genai  # Google Generative AI for generating summaries
from youtube_transcript_api import YouTubeTranscriptApi  # To fetch YouTube video transcript
from youtube_transcript_api.formatters import TextFormatter  # For converting transcript data into a plain-text format

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load proxy from .env
proxy_url = os.getenv("PROXY_URL")
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

# Define prompt for Gemini
prompt = """You are a highly skilled YouTube video summarizer with expertise in extracting key insights and important details from video transcripts. Your task is to carefully analyze the provided transcript of the video and produce a concise yet comprehensive summary. Focus on identifying the main ideas, critical moments, and key takeaways from the video content. The summary should be structured in bullet points, with each point highlighting a distinct aspect of the video.

Your summary should be:

1. Clear and easy to understand, presenting the most relevant information in an organized manner.
2. Concise, keeping the total length under 250 words.
3. Focused on the core themes and ideas of the video, leaving out unnecessary details while retaining the essence of the content.
4. Structured in a way that makes it easy for someone to quickly grasp the video's main points and important takeaways.
5. Provide any action items, recommendations, or conclusions mentioned in the video that can be useful for the viewer."""

# Function to extract transcript
def extract_transcript_details(youtube_video_url, language='en'):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language], proxies=proxies)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to summarize using Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App UI
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")
language = st.selectbox("Select Transcript Language", ["en", "hi", "es", "fr", "de", "it"])

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link, language)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
    except Exception as e:
        if "Could not retrieve a transcript" in str(e):
            st.error("❌ Could not retrieve transcript. YouTube may be blocking requests from this server's IP. Try using a different proxy or run locally.")
        else:
            st.error(f"⚠️ An unexpected error occurred: {e}")
