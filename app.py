from flask import Flask, render_template, request
from markupsafe import Markup
from fetchComments import raw_comments
from utils import get_sentiment_summary
from ytSearch import youtube_search
from analyzeSentiment import clean_comments
import traceback
import sys
import re

app = Flask(__name__)

# Add custom filter to clean up any unwanted tags
@app.template_filter('clean_html')
def clean_html(text):
    if text:
        # Remove unnecessary tags or tag errors
        text = re.sub(r'</?h3>Sentiment Analysis Summary(</?h3>)?', '<h3>Sentiment Analysis Summary</h3>', text)
        text = re.sub(r'</?h3>Comment Summary(</?h3>)?', '<h3>Comment Summary</h3>', text)
        text = re.sub(r'</?strong>Overall sentiment:(</?strong>)?', '<strong>Overall sentiment:</strong>', text)
        text = re.sub(r'</?strong>Based on analyzing \d+ comments:(</?strong>)?', '<strong>Based on analyzing comments:</strong>', text)
    return Markup(text) if text else ""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        categories_str = request.form.get('categories', '')
        print(f"Form data received - Query: '{query}', Categories: '{categories_str}'")
        
        categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
        print(f"Processed categories: {categories}")

        if not query:
            return render_template('index.html', results=[], error='Please enter a search query.')

        try:
            print("Starting YouTube search...")
            all_videos = youtube_search(query)
            print(f"YouTube search results: {len(all_videos)} videos found")
            
            # Limit to top 3 videos for analysis
            videos = all_videos[:3]
            print(f"Limited to top 3 videos for analysis")
            
            results = []
            
            # Process each video individually
            for video in videos:
                if 'video_id' in video:
                    video_id = video['video_id']
                    video_title = video.get('video_title', 'No Title')
                    
                    print(f"Processing video: {video_title} (ID: {video_id})")
                    
                    # Get comments for this specific video (function now only fetches up to 100 comments)
                    print(f"Fetching comments for video ID: {video_id}")
                    video_comments = raw_comments([video_id])  # Pass as a list of one video ID
                    
                    if not video_comments:
                        print(f"No comments found for video ID: {video_id}")
                        sentiment_summary = "No comments available for analysis."
                    else:
                        print(f"Fetched {len(video_comments)} comments for video ID: {video_id}")
                        
                        # Clean the comments (function now only processes up to 100 comments)
                        print("Cleaning comments...")
                        cleaned_comments = clean_comments(video_comments)
                        print(f"Cleaned {len(cleaned_comments)} comments")
                        
                        # Generate sentiment summary for this specific video
                        print(f"Generating sentiment summary for video ID: {video_id}")
                        sentiment_summary = get_sentiment_summary(cleaned_comments, categories)
                        print(f"Sentiment summary generated for video ID: {video_id}")
                    
                    # Create result for this video
                    result = {
                        'video_id': video_id,
                        'title': video_title,
                        'thumbnail': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                        'sentiment': sentiment_summary
                    }
                    
                    results.append(result)
                    print(f"Added result for video ID: {video_id}")
            
            print(f"Processed {len(results)} videos")
            return render_template('index.html', results=results, query=query, categories=','.join(categories))
        
        except KeyError as e:
            error_msg = f'Data format error: {str(e)}'
            print(f"KeyError: {error_msg}")
            traceback.print_exc()
            return render_template('index.html', results=[], error=error_msg)
        except Exception as e:
            error_msg = f'An unexpected error occurred: {str(e)}'
            print(f"Exception: {error_msg}")
            traceback.print_exc()
            return render_template('index.html', results=[], error=error_msg)

    return render_template('index.html', results=[])

if __name__ == '__main__':
    app.run(debug=True)