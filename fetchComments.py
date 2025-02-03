import googleapiclient.discovery
from googleapiclient.errors import HttpError



def raw_comments(video_ids):
    api_key = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    comments = []
    for video_id in video_ids:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=1
            ).execute()
            if not response['items']:
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
                continue

            next_page_token = None
            while True:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=next_page_token,
                    maxResults=100
                ).execute()

                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

        except HttpError as e:
            if e.resp.status == 403 and "commentsDisabled" in str(e):
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
            else:
                print(f"An error occurred while fetching comments for video with ID: {video_id}")
                print(f"Error details: {str(e)}")

    return comments
