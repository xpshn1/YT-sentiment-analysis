from googleapiclient.discovery import build




def youtube_search(query):
    DEVELOPER_KEY = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video = {
            'video_title': search_result['snippet']['title'],
            'video_id': search_result['id']['videoId'],
            'video_url': f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        }
        videos.append(video)

    return videos