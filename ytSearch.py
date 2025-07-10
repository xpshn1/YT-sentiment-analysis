from googleapiclient.discovery import build
import traceback
import os


def youtube_search(query):
    DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY')
    if not DEVELOPER_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable not set.")
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=10
        ).execute()
        
        # Debug: Print the structure of the first result to understand the API response
        if 'items' in search_response and len(search_response['items']) > 0:
            first_item = search_response['items'][0]
            print(f"First search result structure: {first_item.keys()}")
            if 'id' in first_item:
                print(f"ID structure: {first_item['id'].keys()}")

        videos = []
        for search_result in search_response.get('items', []):
            try:
                # Check if the required keys exist
                if 'id' in search_result and 'videoId' in search_result['id'] and 'snippet' in search_result:
                    video = {
                        'video_title': search_result['snippet']['title'],
                        'video_id': search_result['id']['videoId'],
                        'video_url': f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
                    }
                    videos.append(video)
                else:
                    # Print what's missing for debugging
                    print(f"Skipping a result due to missing keys. Available keys: {search_result.keys()}")
                    if 'id' in search_result:
                        print(f"ID keys: {search_result['id'].keys()}")
            except Exception as e:
                print(f"Error processing a search result: {str(e)}")
                continue
                
        print(f"Processed {len(videos)} valid videos")
        return videos
    except Exception as e:
        print(f"Error in YouTube search: {str(e)}")
        traceback.print_exc()
        return []