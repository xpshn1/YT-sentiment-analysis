# YouTube Comment Sentiment Analysis

A Flask web application that searches for YouTube videos and analyzes their comments for sentiment using TextBlob and Google's Gemini API.

## Features

- Search for YouTube videos by keyword
- Analyze top 3 videos with up to 100 comments each
- Calculate sentiment statistics (positive, negative, neutral percentages)
- Generate AI-powered summaries of comment themes and opinions using Gemini API
- Clean, modern UI with responsive design

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd yt_sentiment_analysis
```

2. Create and activate a virtual environment:
```
python -m venv myenv
# On Windows
myenv\Scripts\activate 
# On macOS/Linux
source myenv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up API keys:
   - YouTube Data API key (for video search and comments)
   - Google Gemini API key (for AI-powered sentiment summaries)

## Usage

1. Run the application:
```
python app.py
```

2. Open a web browser and go to `http://127.0.0.1:5000/`

3. Enter a search query and sentiment categories (comma-separated)

4. Click "Analyze Sentiment" to see the results

## Project Structure

- `app.py`: Main Flask application file
- `ytSearch.py`: YouTube search functionality
- `fetchComments.py`: YouTube comment fetching
- `analyzeSentiment.py`: Comment cleaning and basic sentiment analysis
- `utils.py`: Sentiment summary generation with Gemini API
- `static/css/index.css`: Application styling
- `templates/index.html`: HTML template for the web interface

## Dependencies

- Flask: Web framework
- google-api-python-client: YouTube API access
- textblob: Basic sentiment analysis
- google-generativeai: Gemini API for AI summaries
- transformers/pytorch: Advanced NLP capabilities
- Other dependencies in requirements.txt

## Notes

- The application limits analysis to 100 comments per video to improve efficiency
- Gemini API provides detailed text summaries of comments when available
- If the Gemini API fails, the app falls back to basic statistical analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details. 