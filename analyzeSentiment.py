import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def clean_comments(comments):
    """
    Clean and filter comments for sentiment analysis.
    Only processes up to 100 comments to improve efficiency.
    """
    # Return early if no comments
    if not comments:
        return []
        
    # Only process up to 100 comments
    comments_to_process = comments[:100]
    
    # Print a few examples for debugging
    if len(comments_to_process) > 0:
        print(f"Sample comments (first 3):")
        for i, comment in enumerate(comments_to_process[:3]):
            print(f"  {i+1}. {comment[:100]}{'...' if len(comment) > 100 else ''}")
    
    print(f"Cleaning {len(comments_to_process)} comments...")
    cleaned = [comment.strip() for comment in comments_to_process if comment and len(comment.strip()) > 0]
    print(f"After cleaning: {len(cleaned)} valid comments")
    
    return cleaned


def get_sentiment_scores(comments, categories):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Initialize sentiment scores dictionary with empty lists for each category
    sentiment_scores = {category: [] for category in categories}
    
    # If no categories provided, use default positive/negative
    if not categories:
        categories = ["Positive", "Negative"]
        sentiment_scores = {category: [] for category in categories}

    for comment in comments:
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probabilities = outputs.logits.softmax(dim=1).tolist()[0]
        
        # DistilBERT gives [negative, positive] scores
        negative_score = probabilities[0]
        positive_score = probabilities[1]
        
        # Assign scores to appropriate categories
        for category in categories:
            category_lower = category.lower()
            if "positive" in category_lower:
                sentiment_scores[category].append(positive_score)
            elif "negative" in category_lower:
                sentiment_scores[category].append(negative_score)
            elif "neutral" in category_lower:
                # Calculate neutral as 1 - (positive + negative)
                neutral_score = 1 - abs(positive_score - negative_score)
                sentiment_scores[category].append(neutral_score)
            else:
                # For custom categories, just use positive score as default
                sentiment_scores[category].append(positive_score)

    return sentiment_scores