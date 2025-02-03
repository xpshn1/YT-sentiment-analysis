from transformers import AutoModelForSequenceClassification, AutoTokenizer
from googleapiclient.discovery import build
import os
from openai import OpenAI


# Setup for YouTube API

def youtube_search(query, max_results=10):
    DEVELOPER_KEY = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'  # Make sure to replace 'YOUR_API_KEY' with your actual YouTube API key
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=query, type='video', part='id,snippet', maxResults=max_results).execute()
    videos = [{'video_title': item['snippet']['title'], 'video_id': item['id']['videoId']} for item in search_response.get('items', [])]
    return videos

def fetch_comments(video_ids):
    DEVELOPER_KEY = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'  # Make sure to replace 'YOUR_API_KEY' with your actual YouTube API key
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    comments = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    for video_id in video_ids:
        # Fetch and handle comments, including pagination
        pass

def clean_comments(comments):
    print(comments[:10])
    print("____________________________________________________________________________")
    print([comment.strip() for comment in comments][:1])
    return [comment.strip() for comment in comments][:100]

def get_sentiment_summary(comments, categories):
    # Ensure API Key is set
    api_key = "sk-proj-Q0oYhs4s8ZClC8W1JMi0T3BlbkFJ5GxSnlbiku2Kg6XVlZM1"
    if not api_key:
        raise ValueError("API key is not set.")

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Prepare the prompt for the model
    categories_str = ', '.join(categories)  # Format categories list to a string
    prompt = f"Acts as a sentiment summarizer, and summarize the comments. In the summary talk about the sentiment trends in the following categories - {categories_str}, for the comments obtained from the comment section of a youtube video."

    # Join the list of comments into a single string
    comments_str = " ".join(comments)

    # Send the prompt to the model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": comments_str},
        ]
    )

    # Return the model's response
    return response.choices[0].message.content
