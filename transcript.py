import streamlit as st  # Streamlit for creating the web app interface
from dotenv import load_dotenv  # To load environment variables from a .env file

import os  # To access environment variables

import google.generativeai as genai  # Google Generative AI for generating summaries

from youtube_transcript_api import YouTubeTranscriptApi  # To fetch YouTube video transcript

from youtube_transcript_api.formatters import TextFormatter # For converting transcript data into a plain-text format

# Load environment variables from a .env file
load_dotenv()  ## This loads all environment variables defined in the .env file

# Configure Google Generative AI with the API key from environment variables
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Define the prompt for summarizing the YouTube transcript
prompt = """You are a highly skilled YouTube video summarizer with expertise in extracting key insights and important details from video transcripts. Your task is to carefully analyze the provided transcript of the video and produce a concise yet comprehensive summary. Focus on identifying the main ideas, critical moments, and key takeaways from the video content. The summary should be structured in bullet points, with each point highlighting a distinct aspect of the video.

Your summary should be:

1. Clear and easy to understand, presenting the most relevant information in an organized manner.
2. Concise, keeping the total length under 250 words.
3. Focused on the core themes and ideas of the video, leaving out unnecessary details while retaining the essence of the content.
4. Structured in a way that makes it easy for someone to quickly grasp the video's main points and important takeaways.
5. Provide any action items, recommendations, or conclusions mentioned in the video that can be useful for the viewer."""

# Function to extract transcript for non-English videos (e.g., Hindi)
def extract_transcript_details(youtube_video_url, language='en'):
    try:
        # Extract video ID from the YouTube URL
        video_id = youtube_video_url.split("=")[1]

        # Get the transcript of the video using the YouTubeTranscriptApi
        # Specify the language, for example 'hi' for Hindi
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Initialize an empty string to store the complete transcript text
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]  # Append each segment of transcript text

        return transcript  # Return the complete transcript text

    except Exception as e:
        raise e  # Raise exception if any error occurs during transcript fetching

# Function to generate content summary using Google Gemini Pro model
def generate_gemini_content(transcript_text, prompt):
    # Initialize the Google Gemini Pro generative model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content (summary) using the provided prompt and transcript text
    response = model.generate_content(prompt + transcript_text)
    
    # Return the generated summary text
    return response.text

# Streamlit web app title
st.title("YouTube Transcript to Detailed Notes Converter")

# Input field to enter the YouTube video URL
youtube_link = st.text_input("Enter YouTube Video Link:")

# Dropdown to select language (English, Hindi, etc.)
language = st.selectbox("Select Transcript Language", ["en", "hi", "es", "fr", "de", "it"])

# If a YouTube link is entered, extract the video ID and display the thumbnail
if youtube_link:
    video_id = youtube_link.split("=")[1]  # Extract video ID from the URL
    # Display the thumbnail image of the YouTube video using its video ID
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# Button to trigger the generation of detailed notes
if st.button("Get Detailed Notes"):
    try:
        # Extract the transcript text from the YouTube video using the provided link and language
        transcript_text = extract_transcript_details(youtube_link, language)

        # If transcript is available, generate the summary based on the transcript and the prompt
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)

            # Display the detailed summary in the web app
            st.markdown("## Detailed Notes:")  # Markdown header for the summary section
            st.write(summary)  # Display the generated summary text
            
    except Exception as e:
        # If there is an error, display the error message in the web app
        st.error(f"An error occurred: {e}")
