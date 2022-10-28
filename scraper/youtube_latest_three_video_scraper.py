from bs4 import BeautifulSoup
from config.config import Config
from utils.web_request import WebRequest

config = Config()
web_request = WebRequest()


class YoutubeLatestThreeVideoScraper:
    def get_youtube_latest_three_videos(self, channel_url):
        target_address = channel_url + '/videos'
        response = web_request.requester(target_address)
        document = BeautifulSoup(response.text, 'html.parser')
        # print(document.prettify())
        print('********************************')
        # print(str(document.find('script').prettify()))
        # print(document.find('script').get_text())

        # print(document.select_one('#video-title.yt-simple-endpoint.ytd-grid-video-renderer'))
        # content = document.find(class_='yt-simple-endpoint style-scope ytd-grid-video-renderer')
        print('********************************')
        # print(document.find_all('script')[2].get_text())
        for i in range(len(document.find_all('script'))):
            if str(document.find_all('script')[i].get_text()) in 'Rainbow Friends Origin - Poppy Playtime Animation':
                print(document.find_all('script')[i])
            # print(str(document.find_all('script')[i].get_text()) in 'Rainbow Friends Origin - Poppy Playtime Animation')
        # print(content)
        print('********************************')
        exit(1)
