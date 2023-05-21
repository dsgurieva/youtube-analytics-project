import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
class Video:


    def __init__(self, id_video):

        self.id_video = id_video

        try:
            self.url = f"https://www.youtube.com/watch?v={self.id_video}"
            self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.id_video).execute()

        except HttpError:
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None

        try:
             if not self.video_response["title"]:
                raise KeyError("Ошибка индекса")
        except KeyError:
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None

        else:
            self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.id_video).execute()
            self.url = f"https://www.youtube.com/watch?v={self.id_video}"
            self.title = self.video_response['items'][0]['snippet']['title']
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist

