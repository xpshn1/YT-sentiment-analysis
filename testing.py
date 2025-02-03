from fetchComments import raw_comments
from utils import youtube_search, get_sentiment_summary, clean_comments

query = "Taylor swift"
categories = "Positive, Negative, Neutral"
categories = [category.strip() for category in categories if category.strip()]

videos = youtube_search(query)
video_ids = [video['video_id'] for video in videos]

comments = raw_comments(video_ids)
cleaned_comments = clean_comments(comments)
# sentiment_summary = get_sentiment_summary(cleaned_comments, categories)