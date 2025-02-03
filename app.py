from flask import Flask, render_template, request
from fetchComments import raw_comments
from utils import get_sentiment_summary
from ytSearch import youtube_search
from analyzeSentiment import clean_comments


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        categories = [cat.strip() for cat in request.form.get('categories', '').split(',') if cat.strip()]

        if not query:
            return render_template('index.html', results=[], error="Please enter a search query.")

        videos = youtube_search(query)
        video_ids = [video['video_id'] for video in videos]

        comments = raw_comments(video_ids)
        cleaned_comments = clean_comments(comments)
        sentiment_summary = get_sentiment_summary(cleaned_comments, categories)

        results = [
            {
                'video_id': video['video_id'],
                'title': video.get('title', ''),
                'thumbnail': video.get('thumbnail', ''),
                'sentiment': sentiment_summary
            }
            for video in videos
        ]
        return render_template('index.html', results=results, query=query, categories=','.join(categories))

    return render_template('index.html', results=[])

if __name__ == "__main__":
    app.run(debug=True)
