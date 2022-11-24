from config.config import Config
from utils.youtube_channel_statistics_scraper import YoutubeChannelStatisticsScrapper
from utils.data_formatter import DataFormatter

import os

config = Config()
youtube_channel_statistics_scraper = YoutubeChannelStatisticsScrapper()
data_formatter = DataFormatter()


def web_scrape_youtube_channel_statistics():
    data, raw = dict(), dict()
    for s in config.status:
        data[s], raw[s] = dict(), dict()
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            data[s][c], raw[s][c] = list(), list()
            d, r = youtube_channel_statistics_scraper.get_youtube_channels_statistics(c, s)
            data[s][c].extend(d)
            raw[s][c].extend(r)

    if not os.path.isdir(config.data_parent_folder_path):
        os.mkdir(config.data_parent_folder_path)

    for s in config.status:
        if not os.path.isdir(config.channel_statistics_csv_folder_path[s]):
            os.makedirs(config.channel_statistics_csv_folder_path[s])
        if not os.path.isdir(config.channel_statistics_html_folder_path[s]):
            os.makedirs(config.channel_statistics_html_folder_path[s])

    for s in config.status:
        csv_folder_path = config.channel_statistics_csv_folder_path[s]
        raw_folder_path = config.channel_statistics_html_folder_path[s]
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            data_formatter.csv_saver(os.path.join(csv_folder_path, config.csv_filename[s][c]),
                                     config.channel_statistics_header, data[s][c])
            data_formatter.txt_saver(os.path.join(raw_folder_path, config.raw_filename[s][c]), raw[s][c])


if __name__ == '__main__':
    web_scrape_youtube_channel_statistics()
    print('\n\n\nDONE!\n')
