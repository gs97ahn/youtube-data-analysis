from config.config import Config
from api.youtube_api import YoutubeApi
from utils.data_format import DataFormat

import os

config = Config()
youtube_api = YoutubeApi()
data_format = DataFormat()


def youtube_api_videos_and_videos_statistics(target_category):
    youtube_channels = dict()
    youtube_videos_and_video_statistics_csv = dict()
    youtube_videos_txt = dict()
    youtube_video_statistics_txt = dict()
    for status in config.status:
        youtube_channels[status] = dict()
        youtube_videos_and_video_statistics_csv[status] = dict()
        youtube_videos_txt[status] = dict()
        youtube_video_statistics_txt[status] = dict()
        for category in config.categories:
            youtube_channels[status][category] = []
            youtube_videos_and_video_statistics_csv[status][category] = []
            youtube_videos_txt[status][category] = []
            youtube_video_statistics_txt[status][category] = []

    for status in config.status:
        if not os.path.isdir(config.videos_json_folder_path[status]):
            os.makedirs(config.videos_json_folder_path[status])
        if not os.path.isdir(config.video_statistics_json_folder_path[status]):
            os.makedirs(config.video_statistics_json_folder_path[status])
        if not os.path.isdir(config.videos_and_video_statistics_csv_folder_path[status]):
            os.makedirs(config.videos_and_video_statistics_csv_folder_path[status])

    for status in config.status:
        for category in config.categories:
            youtube_channels[status][category] = data_format.csv_reader(
                os.path.join(
                    config.channel_statistics_csv_folder_path[status],
                    config.csv_file_name[status][category]
                )
            )['channel id'].tolist()
            print(youtube_channels[status][category])

    for status in config.status:
        status_csv_folder_path = config.videos_and_video_statistics_csv_folder_path[status]
        status_videos_json_folder_path = config.videos_json_folder_path[status]
        status_video_statistics_json_folder_path = config.video_statistics_json_folder_path[status]
        for category in config.categories:
            if target_category != category:
                continue
            print('\n', status.upper(), category.upper(), '\n')
            for n in range(len(youtube_channels[status][category])):
                videos, videos_raw, video_statistics_raw = youtube_api.videos(youtube_channels[status][category][n])
                youtube_videos_and_video_statistics_csv[status][category].extend(videos)
                youtube_videos_txt[status][category].extend(videos_raw)
                youtube_video_statistics_txt[status][category].extend(video_statistics_raw)
            data_format.csv_saver(
                os.path.join(status_csv_folder_path, config.csv_file_name[status][category]),
                config.videos_and_video_statistics_header,
                youtube_videos_and_video_statistics_csv[status][category]
            )
            data_format.txt_saver(
                os.path.join(status_videos_json_folder_path, config.raw_file_name[status][category]),
                youtube_videos_txt[status][category]
            )
            data_format.txt_saver(
                os.path.join(status_video_statistics_json_folder_path, config.raw_file_name[status][category]),
                youtube_video_statistics_txt[status][category]
            )


def youtube_api_comments(target_category):
    youtube_videos = dict()
    youtube_comments_csv = dict()
    youtube_comments_txt = dict()
    for status in config.status:
        youtube_videos[status] = dict()
        youtube_comments_csv[status] = dict()
        youtube_comments_txt[status] = dict()
        for category in config.categories:
            youtube_videos[status][category] = []
            youtube_comments_csv[status][category] = []
            youtube_comments_txt[status][category] = []

    for status in config.status:
        if not os.path.isdir(config.comments_json_folder_path[status]):
            os.makedirs(config.comments_json_folder_path[status])
        if not os.path.isdir(config.comments_csv_folder_path[status]):
            os.makedirs(config.comments_csv_folder_path[status])

    for status in config.status:
        for category in config.categories:
            youtube_videos[status][category] = data_format.csv_reader(
                os.path.join(
                    config.videos_and_video_statistics_csv_folder_path[status],
                    config.csv_file_name[status][category]
                )
            )['video id'].tolist()
            print(youtube_videos[status][category])

    for status in config.status:
        status_csv_folder_path = config.comments_csv_folder_path[status]
        status_json_folder_path = config.comments_json_folder_path[status]
        for category in config.categories:
            if target_category != category:
                continue
            print('\n', status.upper(), category.upper(), '\n')
            for n in range(len(youtube_videos[status][category])):
                comments, comments_raw = youtube_api.comments(youtube_videos[status][category][n])
                youtube_comments_csv[status][category].extend(comments)
                youtube_comments_txt[status][category].extend(comments_raw)
            data_format.csv_saver(
                os.path.join(status_csv_folder_path, config.csv_file_name[status][category]),
                config.comments_header,
                youtube_comments_csv[status][category]
            )
            data_format.txt_saver(
                os.path.join(status_json_folder_path, config.raw_file_name[status][category]),
                youtube_comments_txt[status][category]
            )


if __name__ == '__main__':
    categories = ['gaming', 'science_and_technology', 'entertainment', 'travel_and_events', 'how_to_and_style',
                  'autos_and_vehicles']
    youtube_api_videos_and_videos_statistics(categories[0])
    youtube_api_comments(categories[0])
    print('\n\n\nDONE!\n\n\n')
