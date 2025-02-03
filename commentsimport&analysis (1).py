

from googleapiclient.discovery import build
from analyzeSentiment import get_sentiment_scores
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import transformers


import googleapiclient.discovery
from googleapiclient.errors import HttpError


def raw_comments(video_id):
    api_key = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'

    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    for video_id in video_id:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=1
            ).execute()

            if not response['items']:
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
                continue

            next_page_token = None
            while True:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=next_page_token,
                    maxResults=100
                ).execute()

                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

        except HttpError as e:
            if e.resp.status == 403 and "commentsDisabled" in str(e):
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
            else:
                print(f"An error occurred while fetching comments for video with ID: {video_id}")
                print(f"Error details: {str(e)}")

    return comments

# Replace VIDEO_ID with the ID of the YouTube video
# The video ID is the part of the URL after "v=" or after "watch?v="
video_id = ['5MuIMqhT8DM']
all_comments=raw_comments(video_id)
print(all_comments)

def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        cleaned_comments.append(comment)
    return cleaned_comments

# You need to install TextBlob first, which you can do using pip:

from textblob import TextBlob

# def get_sentiment_scores(comments):
#     positive_scores = []
#     negative_scores = []
#     for comment in comments:
#         blob = TextBlob(comment)
#         sentiment_score = blob.sentiment.polarity

#         if sentiment_score > 0:
#             positive_scores.append(sentiment_score)
#         elif sentiment_score < 0:
#             negative_scores.append(sentiment_score)

#     return positive_scores, negative_scores

# Replace VIDEO_ID with the ID of the YouTube video
# The video ID is the part of the URL after "v=" or after "watch?v="
video_id = ['5MuIMqhT8DM']
all_comments=raw_comments(video_id)
print(all_comments)

get_sentiment_scores(all_comments)