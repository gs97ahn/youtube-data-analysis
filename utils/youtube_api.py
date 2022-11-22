from config.config import Config
from googleapiclient.discovery import build

import json
import googleapiclient.errors as err

config = Config()


class YoutubeApi:
    def videos(self, channel_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.search().list(part='snippet', channelId=channel_id, maxResults='5', order='date',
                                        type='video')
        v_response = request.execute()

        v_and_vs = list()
        v_raw = json.dumps(v_response, sort_keys=True, indent=4)
        vs_raw = ''
        for v in range(len(v_response['items'])):
            channel_id = v_response['items'][v]['snippet']['channelId']
            video_id = v_response['items'][v]['id']['videoId']
            title = v_response['items'][v]['snippet']['title']
            published_at = v_response['items'][v]['snippet']['publishedAt']
            thumbnail_url = v_response['items'][v]['snippet']['thumbnails']['high']['url']

            vs_response, raw = self.video_statistics(video_id)
            vs_raw += raw + '\n\n\n'
            vs = [channel_id, video_id, title, published_at, thumbnail_url, vs_response[0], vs_response[1],
                  vs_response[2], vs_response[3]]
            v_and_vs.append(vs)
            print(vs)
        return v_and_vs, v_raw, vs_raw

    def video_statistics(self, video_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.videos().list(part='statistics', id=video_id)
        response = request.execute()

        raw = json.dumps(response, sort_keys=True, indent=4)

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
        vs = [comment_count, favorite_count, like_count, view_count]
        return vs, raw

    def comments(self, video_id):
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        request = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults='100', order='time')
        raw = ''
        try:
            response = request.execute()
            raw = json.dumps(response, sort_keys=True, indent=4)
        except err.HttpError as error:
            if error.reason == 'One or more of the requested comment threads cannot be retrieved due to insufficient ' \
                               'permissions. The request might not be properly authorized.':
                print('ERROR: ' + video_id + ' insufficient permissions')
                return [], []
            elif error.reason.split('has ')[1].strip('.') == 'disabled comments':
                print('ERROR: ' + video_id + ' disabled comments')
                return [], []
            else:
                print('ERROR: ' + error.error_details)
                exit(1)

        c = []
        for comment in range(len(response['items'])):
            author_name = response['items'][comment]['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_text = response['items'][comment]['snippet']['topLevelComment']['snippet']['textOriginal']
            like_count = response['items'][comment]['snippet']['topLevelComment']['snippet']['likeCount']
            updated_at = response['items'][comment]['snippet']['topLevelComment']['snippet']['updatedAt']
            c.append([video_id, author_name, comment_text, like_count, updated_at])
        print(c)
        return c, raw
