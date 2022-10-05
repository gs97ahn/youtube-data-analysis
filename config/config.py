from datetime import datetime


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

        # Main URL
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
        self.request_sleep_secs = [10, 30, 60, 180, 300, 600, 1]

        # Data folder and file name
        self.data_parent_folder_path = './data/'

        # Current date
        self.date = datetime.today().strftime('_%Y-%m-%d')

        # CSV
        self.status_category_statistics_csv_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'statistics/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'statistics/' + self.status[1] + '/'
        }
        self.youtube_channel_statistics_csv_file_name = {
            self.status[0]: {
                self.categories[0]: 'gaming_category_statistics' + self.date + '.csv',
                self.categories[1]: 'science_and_technology_category_statistics' + self.date + '.csv',
                self.categories[2]: 'entertainment_category_statistics' + self.date + '.csv',
                self.categories[3]: 'travel_and_events_category_statistics' + self.date + '.csv',
                self.categories[4]: 'how_to_and_style_category_statistics' + self.date + '.csv',
                self.categories[5]: 'autos_and_vehicles_category_statistics' + self.date + '.csv'
            },
            self.status[1]: {
                self.categories[0]: 'gaming_category_channel_statistics' + self.date + '.csv',
                self.categories[1]: 'science_and_technology_category_channel_statistics' + self.date + '.csv',
                self.categories[2]: 'entertainment_category_channel_statistics' + self.date + '.csv',
                self.categories[3]: 'travel_and_events_category_channel_statistics' + self.date + '.csv',
                self.categories[4]: 'how_to_and_style_category_channel_statistics' + self.date + '.csv',
                self.categories[5]: 'autos_and_vehicles_category_channel_statistics' + self.date + '.csv'
            }
        }
        self.youtube_channel_statistics_header = [
            'rank',
            'channel name',
            'current subscriber',
            'subscriber change rate',
            'average views',
            'views change rate',
            'noxinfluencer channel uri',
            'youtube channel url'
        ]

        # HTML
        self.status_category_statistics_html_folder_path = {
            self.status[0]: self.data_parent_folder_path + 'html/' + self.status[0] + '/',
            self.status[1]: self.data_parent_folder_path + 'html/' + self.status[1] + '/'
        }
        self.youtube_channel_statistics_html_file_name = {
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


