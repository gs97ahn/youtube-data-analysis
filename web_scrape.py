from config.config import Config
from utils.youtube_channel_statistics_scraper import YoutubeChannelStatisticsScrapper
from utils.data_format import DataFormat

import os

config = Config()
youtube_channel_statistics_scraper = YoutubeChannelStatisticsScrapper()
data_format = DataFormat()


def web_scrape_youtube_channel_statistics():
    youtube_channels_statistics_csv = dict()
    youtube_channels_statistics_txt = dict()
    for status in config.status:
        youtube_channels_statistics_csv[status] = dict()
        youtube_channels_statistics_txt[status] = dict()
        for category in config.categories:
            youtube_channels_statistics_csv[status][category] = []
            youtube_channels_statistics_txt[status][category] = []

    for status in config.status:
        for category in config.categories:
            print('\n', status.upper(), category.upper(), '\n')
            channel_statistics, raw = youtube_channel_statistics_scraper.get_youtube_channels_statistics(category,
                                                                                                         status)
            youtube_channels_statistics_csv[status][category].extend(channel_statistics)
            youtube_channels_statistics_txt[status][category].extend(raw)

    if not os.path.isdir(config.data_parent_folder_path):
        os.mkdir(config.data_parent_folder_path)

    for status in config.status:
        if not os.path.isdir(config.channel_statistics_csv_folder_path[status]):
            os.makedirs(config.channel_statistics_csv_folder_path[status])
        if not os.path.isdir(config.channel_statistics_html_folder_path[status]):
            os.makedirs(config.channel_statistics_html_folder_path[status])

    for status in config.status:
        status_csv_folder_path = config.channel_statistics_csv_folder_path[status]
        status_html_folder_path = config.channel_statistics_html_folder_path[status]
        for category in config.categories:
            print('\n', status.upper(), category.upper(), '\n')
            data_format.csv_saver(
                os.path.join(status_csv_folder_path, config.csv_file_name[status][category]),
                config.channel_statistics_header,
                youtube_channels_statistics_csv[status][category]
            )
            data_format.txt_saver(
                os.path.join(status_html_folder_path, config.raw_file_name[status][category]),
                youtube_channels_statistics_txt[status][category]
            )


if __name__ == '__main__':
    web_scrape_youtube_channel_statistics()
    print('\n\n\nDONE!\n\n\n')
