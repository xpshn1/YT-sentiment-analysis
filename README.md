# YouTube Comment Sentiment Analysis

A Flask web application designed to search for YouTube videos based on user queries, retrieve comments from these videos, and perform sentiment analysis to provide insights into public opinion.

## Project Goal

The primary goal of this application is to offer users a quick and efficient way to understand the overall sentiment and key opinions expressed in YouTube video comments without needing to manually read through them. It aims to provide both quantitative (sentiment statistics) and qualitative (AI-generated summaries) feedback.

## Features

-   **YouTube Video Search:** Allows users to search for videos using keywords.
-   **Comment Analysis:** Analyzes comments from the top 3 search results.
-   **Sentiment Statistics:** Calculates positive, negative, and neutral comment percentages using TextBlob for initial assessment and a `transformers` model for more detailed scoring.
-   **AI-Powered Summaries:** Leverages Google's Gemini API to generate concise summaries of common themes, opinions, and topics discussed in the comments.
-   **Customizable Sentiment Categories:** Users can define categories for sentiment analysis (defaults to Positive, Negative, Neutral).
-   **User-Friendly Interface:** Clean and responsive web UI for easy interaction.

## Technologies Used

-   **Backend:**
    -   Python 3
    -   Flask (web framework)
-   **Frontend:**
    -   HTML5
    -   CSS3
    -   JavaScript (for minor dynamic behavior like loading indicators)
-   **APIs:**
    -   YouTube Data API v3 (for video search and comment retrieval)
    -   Google Gemini API (for AI-driven comment summarization)
-   **Sentiment Analysis & NLP Libraries:**
    -   `TextBlob`: For quick, polarity-based sentiment scores.
    -   `transformers` (Hugging Face): Utilizes the `distilbert-base-uncased-finetuned-sst-2-english` model for more nuanced sentiment analysis.
    -   `google-generativeai`: Python SDK for the Gemini API.
-   **Core Python Libraries:**
    -   `google-api-python-client`: To interact with Google APIs.
    -   `requests` (and its dependencies like `urllib3`): For making HTTP requests.

## Core Functionality

1.  **User Input:** The user enters a search query and optional sentiment categories through the web interface.
2.  **Video Search:** The Flask application calls `ytSearch.py` to fetch relevant YouTube videos using the YouTube Data API.
3.  **Comment Retrieval:** For the top 3 videos, `fetchComments.py` is used to retrieve up to 100 comments per video.
4.  **Comment Cleaning:** Comments are processed by `analyzeSentiment.py` to remove unnecessary characters and prepare them for analysis.
5.  **Sentiment Analysis:**
    -   `analyzeSentiment.py` uses a `transformers` model to assign sentiment scores to cleaned comments based on the specified categories.
    -   `utils.py` uses `TextBlob` for a basic statistical breakdown (positive/negative/neutral counts).
    -   `utils.py` then sends a sample of comments and the statistical breakdown to the Google Gemini API to generate a qualitative summary.
6.  **Results Display:** The Flask app (`app.py`) renders the results, including video embeds, titles, and the generated sentiment analysis (both stats and Gemini summary), on the `index.html` page.

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
source venv/bin/activate
```

3.  **Install Dependencies:**
    The `requirements.txt` file may have encoding issues (UTF-16 LE with BOM). Ensure it is saved as UTF-8 before running:
    ```bash
    pip install -r requirements.txt
    ```
    *(If you encounter issues, open `requirements.txt` in a text editor, save it with UTF-8 encoding, and try again.)*

4.  **API Key Configuration:**
    This application requires API keys for both the YouTube Data API and the Google Gemini API.

    **IMPORTANT SECURITY NOTICE:** The provided source code contains placeholder API keys directly embedded in files (`ytSearch.py`, `fetchComments.py`, `utils.py`). **These are NOT secure and will likely not work or will be quickly disabled.** You MUST replace them with your own valid API keys.

    -   **YouTube Data API Key:**
        -   Obtain a key from the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
        -   Enable the "YouTube Data API v3".
        -   Replace the placeholder `DEVELOPER_KEY = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'` in:
            -   `ytSearch.py`
            -   `fetchComments.py`
            -   `utils.py` (within the `youtube_search` and `fetch_comments` functions, though these appear to be duplicates of the ones in their respective modules and might be unused or for testing).
    -   **Google Gemini API Key:**
        -   Obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).
        -   Replace the placeholder `api_key = "YOUR_GEMINI_API_KEY"` (or similar, e.g., `AIzaSyDOnmmajGfJh1ssDfJq0wzQ0qbgamzO-ck`) in:
            -   `utils.py` (within the `get_sentiment_summary` function).

    **Recommendation:** For better security and manageability, consider using environment variables to store your API keys instead of hardcoding them. You would then modify the Python scripts to read these keys from the environment.

## Usage

1.  **Run the Flask Application:**
    ```bash
    python app.py
    ```

2.  **Access in Browser:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

3.  **Perform Analysis:**
    -   Enter your search query for YouTube videos.
    -   Optionally, modify the comma-separated sentiment categories (default: "Positive, Negative, Neutral").
    -   Click "Analyze Sentiment".
    -   Wait for the results. The application will display the top 3 videos with their sentiment analysis.

## Project Structure

For a detailed directory tree and component interaction flow, please refer to `PROJECT_STRUCTURE.md`. Key files include:

-   `app.py`: The main Flask application that handles routing and orchestrates the analysis.
-   `ytSearch.py`: Handles searching for videos on YouTube.
-   `fetchComments.py`: Responsible for fetching comments from YouTube videos.
-   `analyzeSentiment.py`: Cleans comments and performs sentiment scoring using a `transformers` model.
-   `utils.py`: Provides utility functions, primarily for generating sentiment summaries using TextBlob and the Google Gemini API.
-   `templates/index.html`: The main HTML template for the user interface.
-   `static/`: Contains CSS stylesheets and images.
-   `requirements.txt`: Lists the Python dependencies.

## Sentiment Analysis Process

1.  **Comment Fetching & Cleaning:** Up to 100 comments are fetched per video and then cleaned (whitespace, etc.).
2.  **Transformer-based Scoring:** The `analyzeSentiment.py` script uses the `distilbert-base-uncased-finetuned-sst-2-english` model to provide nuanced sentiment scores for each comment based on the defined categories.
3.  **TextBlob Statistical Analysis:** `utils.py` uses `TextBlob` to quickly categorize comments into positive, negative, or neutral based on polarity scores, generating overall statistics (e.g., 60% positive).
4.  **Gemini AI Summarization:** A sample of the comments, along with the TextBlob statistics, is sent to the Google Gemini API. Gemini then generates a 2-3 paragraph natural language summary highlighting key themes, opinions, and topics discussed in the comments.
5.  **Fallback:** If the Gemini API call fails, the application falls back to displaying only the statistical summary from TextBlob.

## Limitations

-   **Number of Videos/Comments:** Analysis is currently limited to the top 3 videos from a search and a maximum of 100 comments per video. This is to manage API quota usage and processing time.
-   **API Quotas & Costs:** Extensive use may incur costs or hit rate limits for the YouTube Data API and Google Gemini API. Users should monitor their own API usage.
-   **Sentiment Nuance:** While `transformers` models are more advanced than simple polarity, sentiment analysis (especially AI summarization) can still miss sarcasm, context, or complex nuances.
-   **Hardcoded API Keys:** As mentioned, the default keys are placeholders and a security risk. Users **must** configure their own.

## Scalability and Future Features

**Potential for Scaling:**

-   **Asynchronous Operations:** Implement tasks like API calls for comment fetching and sentiment analysis asynchronously (e.g., using Celery with Flask) to prevent UI blocking and handle larger workloads.
-   **Database Integration:** Store results, video metadata, and perhaps comments in a database to allow for historical analysis, caching, and reduce redundant API calls.
-   **Increased Comment/Video Processing:** With optimized asynchronous processing and database caching, the limits on comments/videos could be gradually increased, keeping API costs in mind.
-   **Load Balancing:** For a high-traffic deployment, use a load balancer and multiple instances of the application.

**Potential Future Features:**

-   **User Accounts:** Allow users to save searches, track analyses, or manage API keys more securely.
-   **Trend Analysis:** Analyze sentiment over time for a specific channel or topic.
-   **Advanced Filtering:** Filter comments by keywords, likes, or commenter activity before analysis.
-   **Comparative Analysis:** Compare sentiment across multiple videos or search queries side-by-side.
-   **Expanded Language Support:** Adapt sentiment analysis for multiple languages (would require different models).
-   **Interactive Visualizations:** Use libraries like Chart.js or D3.js to create more engaging visualizations of sentiment data.
-   **Custom Model Training:** For very specific domains, fine-tune a sentiment analysis model on relevant data.

## Troubleshooting

-   **`ModuleNotFoundError`**: Ensure you have activated your virtual environment and installed all packages from `requirements.txt`.
-   **API Key Errors (401, 403, etc.)**:
    -   Double-check that you have replaced all placeholder API keys in `ytSearch.py`, `fetchComments.py`, and `utils.py` with your own valid keys.
    -   Ensure the respective APIs (YouTube Data API v3, Gemini API) are enabled in your Google Cloud Console/AI Studio.
    -   Check for any billing issues or quota limits reached on your Google Cloud account.
-   **Incorrect `requirements.txt` Encoding**: If `pip install -r requirements.txt` fails with unusual errors, open `requirements.txt`, save it with "UTF-8" encoding, and try again.
-   **"No comments available" / Gemini Summary Fallback**:
    -   The video might have comments disabled.
    -   The Gemini API call might have failed (check `app.py` console output for error messages from `utils.py`). This could be due to an invalid Gemini API key, quota issues, or the model not being available. The app should fall back to TextBlob statistics in this case.
-   **Application Fails to Start**: Check the terminal output where you ran `python app.py` for specific error messages.

## Contributing

While this project is primarily for demonstration, contributions are welcome. Please consider the following if you wish to contribute:
1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Ensure your code follows general Python best practices.
4.  If adding new dependencies, update `requirements.txt`.
5.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
