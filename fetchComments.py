import googleapiclient.discovery
from googleapiclient.errors import HttpError



def raw_comments(video_ids):
    api_key = 'AIzaSyCZI7tkbCHCFVUlthHbtcFfIwrsJ99004w'

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    comments = []
    for video_id in video_ids:
        try:
            # First check if comments are enabled for this video
            print(f"Checking if comments are enabled for video ID: {video_id}")
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=1
            ).execute()
            
            if not response.get('items'):
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
                continue

            # Fetch only up to 100 comments per video to improve efficiency
            print(f"Fetching up to 100 comments for video ID: {video_id}")
            comments_for_video = []
            
            # Get first batch of comments
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100
            ).execute()

            # Process the comments
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments_for_video.append(comment)
                
                # If we've reached 100 comments, stop fetching more
                if len(comments_for_video) >= 100:
                    break
            
            # Only get next page if we still need more comments
            if len(comments_for_video) < 100 and 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
                
                # Get second batch if needed to reach 100 comments
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=next_page_token,
                    maxResults=100
                ).execute()
                
                # Process the comments from second page
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments_for_video.append(comment)
                    
                    # If we've reached 100 comments, stop processing
                    if len(comments_for_video) >= 100:
                        break
            
            # Add the comments from this video to the overall list
            print(f"Fetched {len(comments_for_video)} comments for video ID: {video_id}")
            comments.extend(comments_for_video)

        except HttpError as e:
            if e.resp.status == 403 and "commentsDisabled" in str(e):
                print(f"Comments are disabled for video with ID: {video_id}. Skipping...")
            else:
                print(f"An error occurred while fetching comments for video with ID: {video_id}")
                print(f"Error details: {str(e)}")

    return comments
