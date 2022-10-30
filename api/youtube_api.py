from config.config import Config
from googleapiclient.discovery import build

import json
import time

config = Config()


class YoutubeApi:
    def videos(self, channel_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.search().list(part='snippet',
                                        channelId=channel_id,
                                        maxResults='5',
                                        order='date',
                                        type='video')
        search_response = request.execute()

        videos_and_video_statistics = []
        videos_raw_data = json.dumps(search_response, sort_keys=True, indent=4)
        video_statistics_raw_data = ''
        for video in range(len(search_response['items'])):
            channel_id = search_response['items'][video]['snippet']['channelId']
            video_id = search_response['items'][video]['id']['videoId']
            title = search_response['items'][video]['snippet']['title']
            published_at = search_response['items'][video]['snippet']['publishedAt']
            thumbnail_url = search_response['items'][video]['snippet']['thumbnails']['high']['url']

            videos_response, raw = self.video_statistics(video_id)
            video_statistics_raw_data += raw + '\n\n\n'
            video_info = [channel_id, video_id, title, published_at, thumbnail_url, videos_response[0],
                          videos_response[1], videos_response[2], videos_response[3]]
            videos_and_video_statistics.append(video_info)
            print(video_info)
        return videos_and_video_statistics, videos_raw_data, video_statistics_raw_data

    def video_statistics(self, video_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.videos().list(part='statistics', id=video_id)
        response = request.execute()

        comment_count = '0'
        if 'commentCount' in response['items'][0]['statistics']:
            comment_count = response['items'][0]['statistics']['commentCount']
        favorite_count = '0'
        if 'favoriteCount' in response['items'][0]['statistics']:
            favorite_count = response['items'][0]['statistics']['favoriteCount']
        like_count = '0'
        if 'likeCount' in response['items'][0]['statistics']:
            like_count = response['items'][0]['statistics']['likeCount']
        view_count = '0'
        if 'viewCount' in response['items'][0]['statistics']:
            view_count = response['items'][0]['statistics']['viewCount']
        videos_statistics = [comment_count, favorite_count, like_count, view_count]
        return videos_statistics, json.dumps(response, sort_keys=True, indent=4)

    def comments(self, video_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults='100', order='time')
        response = request.execute()

        comments_raw_data = json.dumps(response, sort_keys=True, indent=4)
        comments = []
        for comment in range(len(response['items'])):
            author_name = response['items'][comment]['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_text = response['items'][comment]['snippet']['topLevelComment']['snippet']['textOriginal']
            like_count = response['items'][comment]['snippet']['topLevelComment']['snippet']['likeCount']
            updated_at = response['items'][comment]['snippet']['topLevelComment']['snippet']['updatedAt']
            comments.append([video_id, author_name, comment_text, like_count, updated_at])
        print(comments)
        return comments, comments_raw_data
