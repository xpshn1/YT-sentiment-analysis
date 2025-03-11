from transformers import AutoModelForSequenceClassification, AutoTokenizer
from googleapiclient.discovery import build
import os
import google.generativeai as genai
import traceback


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

# clean_comments function is now imported from analyzeSentiment module

def get_sentiment_summary(comments, categories):
    import traceback  # Import at function level to avoid scoping issues
    
    try:
        # Ensure API Key is set
        api_key = "AIzaSyDOnmmajGfJh1ssDfJq0wzQ0qbgamzO-ck"  # Google Gemini API key
        if not api_key:
            raise ValueError("API key is not set.")

        # Make sure we have comments to analyze
        if not comments or len(comments) == 0:
            return "No comments available to analyze."
            
        # Make sure we have categories
        if not categories or len(categories) == 0:
            categories = ["Positive", "Negative"]
            
        print(f"Using Gemini API key (first 10 chars): {api_key[:10]}...")
        print(f"Processing {len(comments)} comments for categories: {categories}")

        # First, perform basic sentiment analysis with TextBlob
        from textblob import TextBlob
        
        # Calculate sentiment for each comment
        pos_count = 0
        neg_count = 0
        neutral_count = 0
        
        print("Performing basic sentiment analysis...")
        for comment in comments:  # Analyze all available comments
            blob = TextBlob(comment)
            sentiment = blob.sentiment.polarity
            
            if sentiment > 0.1:
                pos_count += 1
            elif sentiment < -0.1:
                neg_count += 1
            else:
                neutral_count += 1
        
        total = pos_count + neg_count + neutral_count
        pos_percent = (pos_count / total) * 100 if total > 0 else 0
        neg_percent = (neg_count / total) * 100 if total > 0 else 0
        neutral_percent = (neutral_count / total) * 100 if total > 0 else 0
        
        overall_sentiment = 'Mostly positive' if pos_count > neg_count and pos_count > neutral_count else \
                           'Mostly negative' if neg_count > pos_count and neg_count > neutral_count else \
                           'Mostly neutral'
        
        print(f"Basic sentiment analysis completed: {overall_sentiment}")

        # Now try to get a more detailed text summary of comments using Gemini
        try:
            print("Attempting to get comment text summary from Gemini...")
            
            # Configure the Gemini API
            genai.configure(api_key=api_key)
            
            # Try using the newer recommended models directly without checking available models
            # This avoids issues with model discovery and ensures we use a supported model
            
            # Preference order: gemini-1.5-flash (recommended in error), other 1.5 models, fallback models
            preferred_models = [
                "gemini-1.5-flash",  # Recommended in the error message
                "gemini-1.5-pro",    # Another 1.5 series model
                "gemini-1.5-pro-latest", 
                "models/gemini-1.5-flash",
                "models/gemini-pro",  # Fallback to older models if needed
            ]
            
            # Try models in order until one works
            for model_name in preferred_models:
                try:
                    print(f"Attempting to use model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    # Prepare a representative sample of comments for the summary
                    import random
                    sample_size = min(30, len(comments))
                    sample_comments = random.sample(comments, sample_size) if sample_size > 0 else []
                    
                    # Create a text string from the comments
                    comments_text = "\n".join([f"- {comment[:200]}" for comment in sample_comments])
                    
                    # Create a specific prompt for text summarization
                    prompt = f"""
                    I need a detailed summary of the opinions and sentiments expressed in these YouTube comments.
                    Please provide 2-3 concise paragraphs that capture:
                    1. The main points and topics people are discussing
                    2. Specific opinions expressed (both positive and negative)
                    3. Any common themes, complaints, or praise
                    
                    Be specific about the content they're discussing rather than just saying they liked or disliked it.
                    
                    Here are sample comments from the video:
                    
                    {comments_text}
                    
                    Statistics:
                    - Total comments analyzed: {total}
                    - Positive: {pos_count} comments ({pos_percent:.1f}%)
                    - Negative: {neg_count} comments ({neg_percent:.1f}%)
                    - Neutral: {neutral_count} comments ({neutral_percent:.1f}%)
                    - Overall sentiment: {overall_sentiment}
                    """
                    
                    # Get the response from Gemini for a text summary
                    print(f"Sending request to Gemini using model {model_name}...")
                    
                    # Set a timeout and safety settings
                    generation_config = {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": 1024,
                    }
                    
                    # Safety settings might not be supported by all models
                    safety_settings = [
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        }
                    ]
                    
                    try:
                        # Try with safety settings first
                        response = model.generate_content(
                            prompt,
                            generation_config=generation_config,
                            safety_settings=safety_settings
                        )
                    except Exception as config_error:
                        print(f"Error with safety settings: {str(config_error)}")
                        print("Trying without safety settings...")
                        # Try without safety settings if they're not supported
                        response = model.generate_content(
                            prompt,
                            generation_config=generation_config
                        )
                    
                    if response and hasattr(response, 'text'):
                        summary_text = response.text.strip()
                        print(f"Successfully received text summary from Gemini model {model_name}")
                        
                        # Create the complete summary with both statistics and text
                        full_summary = f"""<h3>Sentiment Analysis Summary</h3>

<strong>Based on analyzing {total} comments:</strong>
- Positive: {pos_count} comments ({pos_percent:.1f}%)
- Negative: {neg_count} comments ({neg_percent:.1f}%)
- Neutral: {neutral_count} comments ({neutral_percent:.1f}%)

<strong>Overall sentiment:</strong> {overall_sentiment}

<h3>Comment Summary</h3>
{summary_text}
"""
                        return full_summary
                    else:
                        print(f"Model {model_name} failed to generate text. Trying next model...")
                        continue
                        
                except Exception as model_error:
                    print(f"Error with model {model_name}: {str(model_error)}")
                    print("Trying next model in list...")
                    continue
            
            # If we get here, all models failed
            raise ValueError("All Gemini models failed to generate a summary")
            
        except Exception as gemini_error:
            print(f"Error getting text summary from Gemini: {str(gemini_error)}")
            traceback.print_exc()
            print(f"Falling back to statistics-only summary")
            
            # Fallback to just the statistical summary
            return f"""<h3>Sentiment Analysis Summary</h3>

<strong>Based on analyzing {total} comments:</strong>
- Positive: {pos_count} comments ({pos_percent:.1f}%)
- Negative: {neg_count} comments ({neg_percent:.1f}%)
- Neutral: {neutral_count} comments ({neutral_percent:.1f}%)

<strong>Overall sentiment:</strong> {overall_sentiment}

<p><em>No detailed comment summary available. The sentiment analysis above is based on TextBlob analysis of all {total} comments.</em></p>
"""
            
    except Exception as e:
        print(f"Error in get_sentiment_summary: {str(e)}")
        traceback.print_exc()
        
        # Simple fallback
        return f"Error analyzing sentiment: {str(e)}"
