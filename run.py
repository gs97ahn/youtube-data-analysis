from config.config import Config
from scraper.youtube_channel_scraper import YoutubeChannelScrapper
from utils.data_formatter import DataFormatter

import os

config = Config()
youtube_channel_scrapper = YoutubeChannelScrapper()
data_formatter = DataFormatter()


def web_scrape_youtube_channel_statistics_and_info():
    youtube_channels_statistics_csv = {
        config.status[0]: {
            config.categories[0]: [],
            config.categories[1]: [],
            config.categories[2]: [],
            config.categories[3]: [],
            config.categories[4]: [],
            config.categories[5]: []
        },
        config.status[1]: {
            config.categories[0]: [],
            config.categories[1]: [],
            config.categories[2]: [],
            config.categories[3]: [],
            config.categories[4]: [],
            config.categories[5]: []
        }
    }

    youtube_channels_statistics_txt = {
        config.status[0]: {
            config.categories[0]: [],
            config.categories[1]: [],
            config.categories[2]: [],
            config.categories[3]: [],
            config.categories[4]: [],
            config.categories[5]: []
        },
        config.status[1]: {
            config.categories[0]: [],
            config.categories[1]: [],
            config.categories[2]: [],
            config.categories[3]: [],
            config.categories[4]: [],
            config.categories[5]: []
        }
    }

    for status in config.status:
        for category in config.categories:
            print('\n', status.upper(), category.upper(), '\n')
            channel_statistics, document = youtube_channel_scrapper.get_youtube_channels_statistics(category, status)
            youtube_channels_statistics_csv[status][category].extend(channel_statistics)
            youtube_channels_statistics_txt[status][category].extend(document)

    if not os.path.isdir(config.data_parent_folder_path):
        os.mkdir(config.data_parent_folder_path)

    for status in config.status:
        if not os.path.isdir(config.status_category_statistics_csv_folder_path[status]):
            os.makedirs(config.status_category_statistics_csv_folder_path[status])
        if not os.path.isdir(config.status_category_statistics_html_folder_path[status]):
            os.makedirs(config.status_category_statistics_html_folder_path[status])

    for status in config.status:
        status_csv_folder_path = config.status_category_statistics_csv_folder_path[status]
        status_html_folder_path = config.status_category_statistics_html_folder_path[status]
        for category in config.categories:
            print('\n', status.upper(), category.upper(), '\n')
            for rank in range(config.top_channel_number):
                youtube_channels_statistics_csv[status][category][rank].append(
                    youtube_channel_scrapper.get_youtube_channel_url(
                        youtube_channels_statistics_csv[status][category][rank][6]
                    )
                )
                print(youtube_channels_statistics_csv[status][category][rank])
            data_formatter.csv_saver(
                os.path.join(status_csv_folder_path, config.youtube_channel_statistics_csv_file_name[status][category]),
                config.youtube_channel_statistics_header,
                youtube_channels_statistics_csv[status][category]
            )
            data_formatter.txt_saver(
                os.path.join(status_html_folder_path, config.youtube_channel_statistics_html_file_name[status][category]),
                youtube_channels_statistics_txt[status][category]
            )


if __name__ == '__main__':
    web_scrape_youtube_channel_statistics_and_info()
