

import streamlit as st
from fetchComments import raw_comments
from ytSearch import youtube_search
from utils import youtube_search, get_sentiment_summary, clean_comments

# Setting page configuration
st.set_page_config(page_title="Discourse Engine", page_icon=":movie_camera:", layout="wide")

# Load custom CSS
with open("index.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title and Header
st.image("static/images/youtube-logo-png-2074.png", width=100)
st.title("Discourse Engine")
st.markdown("## YouTube Comment Sentiment Analysis")

# YouTube Video Search
st.header("Search YouTube Videos")
query = st.text_input("Enter search query:")

if st.button("Search"):
    with st.spinner('Fetching results, please wait...'):
        results = youtube_search(query)
        st.write(results)

# Fetch YouTube Comments
st.header("Fetch YouTube Comments")
video_id = st.text_input("Enter YouTube Video ID:")

if st.button("Fetch Comments"):
    with st.spinner('Fetching comments, please wait...'):
        comments = raw_comments(video_id)
        st.write(comments)

# Analyze Sentiment
st.header("Analyze Sentiment")
if st.button("Analyze Sentiment"):
    with st.spinner('Analyzing sentiment, please wait...'):
        processed_comments = clean_comments(comments)
        sentiments = get_sentiment_summary(processed_comments)
        st.write(sentiments)

# Welcome Message
if not query and not video_id:
    st.markdown("""
        <div class="app-info">
            <h2>Welcome to the YouTube Sentiment Analysis App</h2>
            <p>This app allows you to search for YouTube videos and analyzes the sentiment of the comments using zero-shot learning.</p>
            <p>Enter a search query in the search bar above and specify the sentiment categories you want to analyze (comma-separated).</p>
            <p>The app will retrieve relevant videos, analyze the comments using the specified categories, and display the sentiment scores for each category.</p>
        </div>
    """, unsafe_allow_html=True)
