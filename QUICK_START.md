# Quick Start Guide

This guide will help you get the YouTube Sentiment Analysis application up and running quickly.

## Prerequisites

1. Python 3.7+ installed
2. API Keys:
   - YouTube Data API key
   - Google Gemini API key

## Setup

1. **Clone or download the project** to your local machine.

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   The `requirements.txt` file may have encoding issues (UTF-16 LE with BOM). Ensure it is saved as UTF-8 before running:
   ```bash
   pip install -r requirements.txt
   ```
   *(If you encounter issues, open `requirements.txt` in a text editor, save it with UTF-8 encoding, and try again.)*

4. **Configure API keys**:
   **IMPORTANT SECURITY NOTICE:** The provided source code may contain placeholder API keys. **These are NOT secure and will likely not work or will be quickly disabled.** You MUST replace them with your own valid API keys. For detailed instructions on obtaining keys, refer to the main `README.md` file.

   - Open `utils.py` and replace the **Google Gemini API key**:
     ```python
     api_key = "YOUR_GEMINI_API_KEY"  # Replace with your actual key
     ```
   - Open `ytSearch.py` and `fetchComments.py` and replace the **YouTube Data API key**:
     ```python
     DEVELOPER_KEY = 'YOUR_YOUTUBE_API_KEY'  # Replace with your actual key
     ```
   It is highly recommended to use environment variables for API keys in a production environment.

## Running the Application

1. **Start the Flask server**:
   ```
   python app.py
   ```

2. **Access the application** by opening a web browser and navigating to:
   ```
   http://127.0.0.1:5000/
   ```

3. **Use the application**:
   - Enter a search query (e.g., "stock market")
   - Specify sentiment categories (default: Positive, Negative, Neutral)
   - Click "Analyze Sentiment"
   - Wait for the analysis to complete (this may take a minute)
   - Review the sentiment results for each video

## Troubleshooting

- **API Key Issues**: Make sure your API keys are valid and have the necessary permissions
- **Module Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **No Comments Found**: Some videos might have comments disabled
- **Gemini API Errors**: If the Gemini summary fails, the application will fall back to basic statistics

## Next Steps

- Try different search queries to see how sentiment varies
- Experiment with different sentiment categories
- Review the code to understand how the analysis works
- Consider adding your own custom features 