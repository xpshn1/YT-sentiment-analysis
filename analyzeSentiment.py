import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def clean_comments(comments):
    cleaned_comments = []
    for comment in comments:
        cleaned_comments.append(comment)
    return cleaned_comments


def get_sentiment_scores(comments, categories):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    sentiment_scores = {category: [] for category in categories}

    for comment in comments:
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probabilities = outputs.logits.softmax(dim=1).tolist()[0]
        sentiment_score = probabilities[1] - probabilities[0]

        for category in categories:
            sentiment_scores[category].append(sentiment_score)

    return sentiment_scores