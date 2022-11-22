from config.config import Config
from utils.youtube_api import YoutubeApi
from utils.data_formatter import DataFormatter

import os

config = Config()
youtube_api = YoutubeApi()
data_format = DataFormatter()


def youtube_api_videos_and_videos_statistics():
    youtube_channels = dict()
    data = dict()
    video_raw = dict()
    video_statistics_raw = dict()
    for s in config.status:
        youtube_channels[s] = dict()
        data[s] = dict()
        video_raw[s] = dict()
        video_statistics_raw[s] = dict()
        for c in config.categories:
            youtube_channels[s][c] = list()
            data[s][c] = list()
            video_raw[s][c] = list()
            video_statistics_raw[s][c] = list()

    for s in config.status:
        for c in config.categories:
            youtube_channels[s][c] = data_format.csv_reader(os.path.join(
                config.channel_statistics_csv_folder_path[s], config.csv_file_name[s][c]
            ))['channel id'].tolist()
            print(youtube_channels[s][c])

    for s in config.status:
        if not os.path.isdir(config.videos_json_folder_path[s]):
            os.makedirs(config.videos_json_folder_path[s])
        if not os.path.isdir(config.video_statistics_json_folder_path[s]):
            os.makedirs(config.video_statistics_json_folder_path[s])
        if not os.path.isdir(config.videos_and_video_statistics_csv_folder_path[s]):
            os.makedirs(config.videos_and_video_statistics_csv_folder_path[s])

    for s in config.status:
        csv_folder_path = config.videos_and_video_statistics_csv_folder_path[s]
        video_raw_folder_path = config.videos_json_folder_path[s]
        video_statistics_raw_folder_path = config.video_statistics_json_folder_path[s]
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            for i in range(len(youtube_channels[s][c])):
                v_vs_csv, v_raw, vs_raw = youtube_api.videos(youtube_channels[s][c][i])
                data[s][c].extend(v_vs_csv)
                video_raw[s][c].extend(v_raw)
                video_statistics_raw[s][c].extend(vs_raw)

            data_format.csv_saver(os.path.join(csv_folder_path, config.csv_file_name[s][c]),
                                  config.videos_and_video_statistics_header,
                                  data[s][c])
            data_format.txt_saver(os.path.join(video_raw_folder_path, config.raw_file_name[s][c]), video_raw[s][c])
            data_format.txt_saver(os.path.join(video_statistics_raw_folder_path, config.raw_file_name[s][c]),
                                  video_statistics_raw[s][c])


def youtube_api_comments():
    videos = dict()
    data = dict()
    raw = dict()

    for status in config.status:
        videos[status] = dict()
        data[status] = dict()
        raw[status] = dict()
        for category in config.categories:
            videos[status][category] = []
            data[status][category] = []
            raw[status][category] = []

    for status in config.status:
        if not os.path.isdir(config.comments_json_folder_path[status]):
            os.makedirs(config.comments_json_folder_path[status])
        if not os.path.isdir(config.comments_csv_folder_path[status]):
            os.makedirs(config.comments_csv_folder_path[status])

    for s in config.status:
        for c in config.categories:
            videos[s][c] = data_format.csv_reader(os.path.join(config.videos_and_video_statistics_csv_folder_path[s],
                                                               config.csv_file_name[s][c]))['video id'].tolist()
            print(videos[s][c])

    for s in config.status:
        csv_folder_path = config.comments_csv_folder_path[s]
        raw_folder_path = config.comments_json_folder_path[s]
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            for i in range(len(videos[s][c])):
                c_csv, c_raw = youtube_api.comments(videos[s][c][i])
                data[s][c].extend(c_csv)
                raw[s][c].extend(c_raw)

            data_format.csv_saver(os.path.join(csv_folder_path, config.csv_file_name[s][c]), config.comments_header,
                                  data[s][c])
            data_format.txt_saver(os.path.join(raw_folder_path, config.raw_file_name[s][c]), raw[s][c])


if __name__ == '__main__':
    youtube_api_videos_and_videos_statistics()
    youtube_api_comments()
    print('\n\n\nDONE!\n')
