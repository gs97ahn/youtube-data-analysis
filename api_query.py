from config.config import Config
from utils.youtube_api import YoutubeApi
from utils.data_formatter import DataFormatter

import os

config = Config()
youtube_api = YoutubeApi()
data_format = DataFormatter()


def make_folders(folder_path_list):
    for folder_path in folder_path_list:
        for s in config.status:
            if not os.path.isdir(folder_path[s]):
                os.makedirs(folder_path[s])


def youtube_api_videos_and_videos_statistics():
    make_folders([config.cdata_videos_json_folder_path, config.cdata_video_statistics_json_folder_path,
                  config.cdata_videos_and_video_statistics_csv_folder_path])

    youtube_channels = dict()
    for s in config.status:
        youtube_channels[s] = dict()
        for c in config.categories:
            youtube_channels[s][c] = list()
            youtube_channels[s][c] = data_format.csv_reader(os.path.join(
                config.cdata_channel_statistics_csv_folder_path[s], config.csv_filename[s][c]
            ))['channel id'].tolist()

    data, video_raw, video_statistics_raw = dict(), dict(), dict()
    for s in config.status:
        data[s], video_raw[s], video_statistics_raw[s] = dict(), dict(), dict()
        csv_folder_path = config.cdata_videos_and_video_statistics_csv_folder_path[s]
        video_raw_folder_path = config.cdata_videos_json_folder_path[s]
        video_statistics_raw_folder_path = config.cdata_video_statistics_json_folder_path[s]
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            data[s][c], video_raw[s][c], video_statistics_raw[s][c] = list(), list(), list()
            for i in range(len(youtube_channels[s][c])):
                v_vs_csv, v_raw, vs_raw = youtube_api.videos(youtube_channels[s][c][i])
                data[s][c].extend(v_vs_csv)
                video_raw[s][c].extend(v_raw)
                video_statistics_raw[s][c].extend(vs_raw)

            data_format.csv_saver(os.path.join(csv_folder_path, config.csv_filename[s][c]),
                                  config.cdata_videos_and_video_statistics_header,
                                  data[s][c])
            data_format.txt_saver(os.path.join(video_raw_folder_path, config.raw_filename[s][c]), video_raw[s][c])
            data_format.txt_saver(os.path.join(video_statistics_raw_folder_path, config.raw_filename[s][c]),
                                  video_statistics_raw[s][c])


def youtube_api_comments():
    videos = dict()
    for s in config.status:
        videos[s] = dict()
        for c in config.categories:
            videos[s][c] = list()
            videos[s][c] = data_format.csv_reader(os.path.join(
                config.cdata_videos_and_video_statistics_csv_folder_path[s],
                config.csv_filename[s][c])
            )['video id'].tolist()

    make_folders([config.cdata_comments_json_folder_path, config.cdata_comments_csv_folder_path])

    data, raw = dict(), dict()
    for s in config.status:
        data[s], raw[s] = dict(), dict()
        csv_folder_path = config.cdata_comments_csv_folder_path[s]
        raw_folder_path = config.cdata_comments_json_folder_path[s]
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            data[s][c], raw[s][c] = list(), list()
            for i in range(len(videos[s][c])):
                c_csv, c_raw = youtube_api.comments(videos[s][c][i])
                data[s][c].extend(c_csv)
                raw[s][c].extend(c_raw)

            data_format.csv_saver(os.path.join(csv_folder_path, config.csv_filename[s][c]),
                                  config.cdata_comments_header, data[s][c])
            data_format.txt_saver(os.path.join(raw_folder_path, config.raw_filename[s][c]), raw[s][c])


if __name__ == '__main__':
    youtube_api_videos_and_videos_statistics()
    youtube_api_comments()
    print('\n\n\nDONE!\n')
