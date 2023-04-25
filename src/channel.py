import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.description = self.channel['items'][0]['snippet']['description']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def getter_channel_id(self) -> str:
        return self.__channel_id
    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return self.channel

    def to_json(self, path):
        """Метод, сохраняющий в файл значения атрибутов экземпляра Channel"""
        self.path = path
        with open(self.path, 'w') as file:
            return json.dump({
                'title': self.title,
                'description': self.description,
                'videoCount': self.video_count,
                'subscriberCount': self.subscriber_count,
                'viewCount': self.view_count,
                'url': self.url

            }, file, indent=2, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube





