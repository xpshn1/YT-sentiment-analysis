# Project Structure

```
yt_sentiment_analysis/
│
├── app.py                 # Main Flask application
├── utils.py               # Utility functions including sentiment analysis with Gemini API
├── ytSearch.py            # YouTube search functionality
├── fetchComments.py       # YouTube comment fetching
├── analyzeSentiment.py    # Comment cleaning and basic sentiment analysis
│
├── static/                # Static assets
│   ├── css/               # CSS files
│   │   └── index.css      # Main stylesheet
│   │
│   └── images/            # Image assets
│       └── youtube-logo-png-2074.png  # YouTube logo
│
├── templates/             # HTML templates
│   └── index.html         # Main page template
│
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
│
└── myenv/                 # Virtual environment (not in version control)
```

## Key Components Interaction

1. **User Interface Flow:**
   - User enters search query and categories in web interface
   - Flask app processes form submission
   - Results displayed in responsive grid layout

2. **Data Processing Flow:**
   - YouTube search (ytSearch.py) -> Find relevant videos
   - Fetch comments (fetchComments.py) -> Get comments for each video
   - Clean comments (analyzeSentiment.py) -> Prepare text for analysis
   - Sentiment analysis (utils.py) -> Generate statistics and summaries
   - Results display (templates/index.html) -> Show analysis to user

3. **API Integration:**
   - YouTube Data API: For video search and comment retrieval
   - Google Gemini API: For AI-powered comment summarization 