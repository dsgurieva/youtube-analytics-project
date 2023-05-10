import os
from googleapiclient.discovery import build

from datetime import datetime, timedelta
import isodate


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList:


    def __init__(self, id_playlist):
        """
         Инициализирует _id_ плейлиста и имеет следующие публичные атрибуты:
                - название плейлиста
                - ссылку на плейлист
        """
        self.id_playlist = id_playlist
        self.playlist_videos = youtube.playlists().list(part='snippet', id=self.id_playlist).execute()
        self.url = f'https://www.youtube.com/playlist?list={self.id_playlist}'
        self.title = self.playlist_videos['items'][0]['snippet']['title']


    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""

        playlist_videos = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        total_video_time = timedelta(hours=0, minutes=0, seconds=0)

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_video_time += duration

        return total_video_time


    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        playlist_videos = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        max_counter_like = 0
        url = ''

        for video in playlist_videos['items']:
            video_id = video['contentDetails']['videoId']
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            like_count: int = int(video_response['items'][0]['statistics']['likeCount'])

            if like_count > max_counter_like:
                max_counter_like = like_count
                url = f'https://youtu.be/{video_id}'

        return url








