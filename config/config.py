from datetime import datetime

import os


class Config:
    def __init__(self):
        # Youtube Categories
        self.categories = [
            'gaming',
            'science_and_technology',
            'entertainment',
            'travel_and_events',
            'how_to_and_style',
            'autos_and_vehicles'
        ]
        self.status = ['increased', 'decreased']
        self.top_channel_number = 30

        # Web Scraping Related
        # URL
        self.noxinfluencer_url = 'https://www.noxinfluencer.com'

        # Top 100 Increase Subscription by Categories URI
        self.increased_category_urls = {
            self.categories[0]: self.noxinfluencer_url + '/youtube-channel-rank/top-100-us-gaming-youtuber-sorted-by-'
                                                         'growth-weekly',
            self.categories[1]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-science%20%26%20technology-youtuber-sorted-by-'
                                                         'growth-weekly',
            self.categories[2]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-entertainment-youtuber-sorted-by-growth-weekly',
            self.categories[3]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-travel%20%26%20events-youtuber-sorted-by-'
                                                         'growth-weekly',
            self.categories[4]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-howto%20%26%20style-youtuber-sorted-by-'
                                                         'growth-weekly',
            self.categories[5]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-autos%20%26%20vehicles-youtuber-sorted-by-'
                                                         'growth-weekly'
        }

        # Top 100 Decrease Subscription by Categories URI
        self.decreased_category_urls = {
            self.categories[0]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-gaming-youtuber-sorted-by-decrease-weekly',
            self.categories[1]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-science%20%26%20technology-youtuber-sorted-by-'
                                                         'decrease-weekly',
            self.categories[2]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-entertainment-youtuber-sorted-by-decrease-weekly',
            self.categories[3]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-travel%20%26%20events-youtuber-sorted-by-'
                                                         'decrease-weekly',
            self.categories[4]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-howto%20%26%20style-youtuber-sorted-by-'
                                                         'decrease-weekly',
            self.categories[5]: self.noxinfluencer_url + '/youtube-channel-rank'
                                                         '/top-100-us-autos%20%26%20vehicles-youtuber-sorted-by-'
                                                         'decrease-weekly'
        }

        # Cookies
        self.cookies = {'customLanguage': 'EN'}

        # Time Sleep
        self.request_sleep_secs = [5, 10, 30, 60, 300, 600, 1]

        # Data folder and file name
        self.data_parent_folder_path = './data/'

        # Current date
        self.date = datetime.today().strftime('_%Y-%m-%d')

        # CSV File Name
        self.csv_file_name = {
            self.status[0]: {
                self.categories[0]: 'gaming_category' + self.date + '.csv',
                self.categories[1]: 'science_and_technology_category' + self.date + '.csv',
                self.categories[2]: 'entertainment_category' + self.date + '.csv',
                self.categories[3]: 'travel_and_events_category' + self.date + '.csv',
                self.categories[4]: 'how_to_and_style_category' + self.date + '.csv',
                self.categories[5]: 'autos_and_vehicles_category' + self.date + '.csv'
            },
            self.status[1]: {
                self.categories[0]: 'gaming_category' + self.date + '.csv',
                self.categories[1]: 'science_and_technology_category' + self.date + '.csv',
                self.categories[2]: 'entertainment_category' + self.date + '.csv',
                self.categories[3]: 'travel_and_events_category' + self.date + '.csv',
                self.categories[4]: 'how_to_and_style_category' + self.date + '.csv',
                self.categories[5]: 'autos_and_vehicles_category' + self.date + '.csv'
            }
        }

        # Raw File Name
        self.raw_file_name = {
            self.status[0]: {
                self.categories[0]: 'gaming_category' + self.date + '.txt',
                self.categories[1]: 'science_and_technology_category' + self.date + '.txt',
                self.categories[2]: 'entertainment_category' + self.date + '.txt',
                self.categories[3]: 'travel_and_events_category' + self.date + '.txt',
                self.categories[4]: 'how_to_and_style_category' + self.date + '.txt',
                self.categories[5]: 'autos_and_vehicles_category' + self.date + '.txt'
            },
            self.status[1]: {
                self.categories[0]: 'gaming_category' + self.date + '.txt',
                self.categories[1]: 'science_and_technology_category' + self.date + '.txt',
                self.categories[2]: 'entertainment_category' + self.date + '.txt',
                self.categories[3]: 'travel_and_events_category' + self.date + '.txt',
                self.categories[4]: 'how_to_and_style_category' + self.date + '.txt',
                self.categories[5]: 'autos_and_vehicles_category' + self.date + '.txt'
            }
        }

        # Channel Statistics
        # CSV
        self.channel_statistics_csv_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'channel_statistics/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'channel_statistics/' + self.status[1] + '/'
        }
        self.channel_statistics_header = [
            'rank',
            'channel name',
            'current subscriber',
            'subscriber change rate',
            'average views',
            'views change rate',
            'channel id',
        ]

        # HTML
        self.channel_statistics_html_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'raw/channel_statistics_html/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'raw/channel_statistics_html/' + self.status[1] + '/'
        }

        # API Related
        # API Key
        self.api_key = os.environ['API_KEY']

        # Videos
        # JSON
        self.videos_json_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'raw/videos_json/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'raw/videos_json/' + self.status[1] + '/'
        }

        # Video Statistics
        # JSON
        self.video_statistics_json_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'raw/video_statistics_json/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'raw/video_statistics_json/' + self.status[1] + '/'
        }

        # Video and Video Statistics
        # CSV
        self.videos_and_video_statistics_csv_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'videos_and_video_statistics/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'videos_and_video_statistics/' + self.status[1] + '/'
        }
        self.videos_and_video_statistics_header = ['channel id', 'video id', 'title', 'published at', 'thumbnail url',
                                                   'comment count', 'favorite count', 'like count', 'view count']

        # Comments
        # JSON
        self.comments_json_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'raw/comments_json/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'raw/comments_json/' + self.status[1] + '/'
        }

        # CSV
        self.comments_csv_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'comments/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'comments/' + self.status[1] + '/'
        }

        # CSV Header
        self.comments_header = ['video id', 'author name', 'comment text', 'like count', 'updated at']
