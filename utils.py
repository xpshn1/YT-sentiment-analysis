from transformers import AutoModelForSequenceClassification, AutoTokenizer
# from googleapiclient.discovery import build # This import is no longer needed.
import os
import google.generativeai as genai
import traceback

# clean_comments function is now imported from analyzeSentiment module

def get_sentiment_summary(comments, categories):
    import traceback  # Import at function level to avoid scoping issues

    try:
        # Ensure API Key is set for Gemini
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if not gemini_api_key:
            # Fallback to basic stats if Gemini key is not set, but log it.
            print("GEMINI_API_KEY environment variable not set. Falling back to TextBlob analysis only.")
            # Perform basic sentiment analysis with TextBlob
            from textblob import TextBlob
            pos_count = 0
            neg_count = 0
            neutral_count = 0
            for comment in comments:
                blob = TextBlob(comment)
                sentiment = blob.sentiment.polarity
                if sentiment > 0.1: pos_count += 1
                elif sentiment < -0.1: neg_count += 1
                else: neutral_count += 1
            total = pos_count + neg_count + neutral_count
            pos_percent = (pos_count / total) * 100 if total > 0 else 0
            neg_percent = (neg_count / total) * 100 if total > 0 else 0
            neutral_percent = (neutral_count / total) * 100 if total > 0 else 0
            overall_sentiment = 'Mostly positive' if pos_count > neg_count and pos_count > neutral_count else \
                               'Mostly negative' if neg_count > pos_count and neg_count > neutral_count else \
                               'Mostly neutral'
            return f"""<h3>Sentiment Analysis Summary</h3>
<strong>Based on analyzing {total} comments:</strong>
- Positive: {pos_count} comments ({pos_percent:.1f}%)
- Negative: {neg_count} comments ({neg_percent:.1f}%)
- Neutral: {neutral_count} comments ({neutral_percent:.1f}%)
<strong>Overall sentiment:</strong> {overall_sentiment}
<p><em>Detailed AI summary unavailable (GEMINI_API_KEY not configured).</em></p>"""

        # Make sure we have comments to analyze
        if not comments or len(comments) == 0:
            return "No comments available to analyze."

        # Make sure we have categories
        if not categories or len(categories) == 0:
            categories = ["Positive", "Negative"] # Default categories

        print(f"Using Gemini API key.") # No longer printing part of the key
        print(f"Processing {len(comments)} comments for categories: {categories}")

        # First, perform basic sentiment analysis with TextBlob
        from textblob import TextBlob

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

            genai.configure(api_key=gemini_api_key) # Use the key from env var

            preferred_models = [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-1.5-pro-latest",
                "models/gemini-1.5-flash",
                "models/gemini-pro",
            ]

            model_successfully_used = False
            for model_name in preferred_models:
                try:
                    print(f"Attempting to use model: {model_name}")
                    model = genai.GenerativeModel(model_name)

                    import random
                    sample_size = min(30, len(comments))
                    sample_comments = random.sample(comments, sample_size) if sample_size > 0 else []
                    comments_text = "\n".join([f"- {comment[:200]}" for comment in sample_comments])

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

                    print(f"Sending request to Gemini using model {model_name}...")
                    generation_config = {
                        "temperature": 0.7, "top_p": 0.9, "top_k": 40, "max_output_tokens": 1024,
                    }
                    safety_settings = [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
                    ]

                    response_text = None
                    try:
                        response = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings)
                        if response and hasattr(response, 'text'): response_text = response.text.strip()
                    except Exception as config_error:
                        print(f"Error with safety settings for model {model_name}: {str(config_error)}. Trying without...")
                        response = model.generate_content(prompt, generation_config=generation_config)
                        if response and hasattr(response, 'text'): response_text = response.text.strip()

                    if response_text:
                        print(f"Successfully received text summary from Gemini model {model_name}")
                        full_summary = f"""<h3>Sentiment Analysis Summary</h3>
<strong>Based on analyzing {total} comments:</strong>
- Positive: {pos_count} comments ({pos_percent:.1f}%)
- Negative: {neg_count} comments ({neg_percent:.1f}%)
- Neutral: {neutral_count} comments ({neutral_percent:.1f}%)
<strong>Overall sentiment:</strong> {overall_sentiment}
<h3>Comment Summary</h3>
{response_text}"""
                        model_successfully_used = True
                        return full_summary
                    else:
                        print(f"Model {model_name} failed to generate text. Trying next model...")

                except Exception as model_error:
                    print(f"Error with model {model_name}: {str(model_error)}")
                    print("Trying next model in list...")

            if not model_successfully_used:
                 raise ValueError("All Gemini models failed to generate a summary or no suitable model found.")

        except Exception as gemini_error:
            print(f"Error getting text summary from Gemini: {str(gemini_error)}")
            traceback.print_exc()
            # Fallback to statistical summary if Gemini fails for any reason
            return f"""<h3>Sentiment Analysis Summary</h3>
<strong>Based on analyzing {total} comments:</strong>
- Positive: {pos_count} comments ({pos_percent:.1f}%)
- Negative: {neg_count} comments ({neg_percent:.1f}%)
- Neutral: {neutral_count} comments ({neutral_percent:.1f}%)
<strong>Overall sentiment:</strong> {overall_sentiment}
<p><em>AI-powered detailed comment summary could not be generated. Error: {str(gemini_error)}</em></p>"""

    except Exception as e:
        print(f"Error in get_sentiment_summary: {str(e)}")
        traceback.print_exc()
        return f"Error analyzing sentiment: {str(e)}"
