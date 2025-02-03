YT Sentiment Analysis
A Python-based web application that performs sentiment analysis on YouTube video comments using GPT-3.5 Turbo and provides both Flask and Streamlit interfaces.

Features
YouTube video search using the YouTube Data API
Comment fetching from multiple videos
Sentiment analysis using GPT-3.5 Turbo
Web interface options using Flask or Streamlit
Support for custom sentiment categories
Core Components
YouTube Integration
The youtube_search function in ytSearch.py handles video searching:

Comment Fetching
Comments are retrieved using the raw_comments function in fetchComments.py.

Sentiment Analysis
Sentiment analysis is performed using OpenAI's GPT-3.5 Turbo through the get_sentiment_summary function in utils.py.

Setup
Install required packages:
Configure API keys:
YouTube API key
OpenAI API key
Usage
Flask Interface
Run the Flask application:

Streamlit Interface
Run the Streamlit application:

Project Structure
app.py - Flask web application
Streamlit.py - Streamlit interface
ytSearch.py - YouTube search functionality
fetchComments.py - Comment fetching
analyzeSentiment.py - Sentiment analysis
utils.py - Utility functions and OpenAI integration
Dependencies
Flask
Streamlit
google-api-python-client
openai
transformers
Security Note
Important: Keep your API keys secure and never commit them to version control.

