from bs4 import BeautifulSoup
from config.config import Config
from utils.web_request import WebRequest

config = Config()
web_request = WebRequest()


class YoutubeChannelStatisticsScrapper:
    def count_format_from_text_to_numeric(self, count):
        if count[-1] == 'K':
            n = float(count[:-1]) * 1000
        elif count[-1] == 'M':
            n = float(count[:-1]) * 1000000
        elif count[-1] == 'B':
            n = float(count[:-1]) * 1000000000
        else:
            n = float(count)
        return int(n)

    def percentage_from_tag_to_float(self, tag):
        if tag.find(class_='change up') is not None:
            n = float(str(tag.find(class_='change up')).split('%')[0].split('</span> ')[1])
        elif tag.find(class_='change down') is not None:
            n = float(str(tag.find(class_='change down')).split('%')[0].split('</span> ')[1]) * -1
        elif tag.find(class_='change none') is not None:
            n = 0.0
        else:
            print('ERROR: unavailable', tag)
            exit(1)
        return n

    def get_youtube_channels_statistics(self, category, status):
        target_address = ''
        if status == 'increased':
            target_address = config.increased_category_urls[category]
        elif status == 'decreased':
            target_address = config.decreased_category_urls[category]
        response = web_request.requester(target_address)
        document = BeautifulSoup(response.text, 'html.parser')
        ycs = []
        rank = 0
        content = document.find(class_='table-body').contents

        for youtuber in range(1, config.top_channel_number * 2, 2):
            rank += 1
            channel_name = str(content[youtuber].find(class_='title pull-left ellipsis').string).strip()
            current_subscriber = str(
                content[youtuber].find(class_='rank-cell pull-left rank-subs').find(class_='number').string
            ).strip()
            current_average_view = str(
                content[youtuber].find(class_='rank-cell pull-left rank-avg-view').find(class_='number').string
            ).strip()
            current_subscriber = int(self.count_format_from_text_to_numeric(current_subscriber))
            current_average_view = int(self.count_format_from_text_to_numeric(current_average_view))
            subscriber_change_rate = content[youtuber].find(class_='rank-cell pull-left rank-subs')
            average_view_change_rate = content[youtuber].find(class_='rank-cell pull-left rank-avg-view')
            subscriber_change_rate = self.percentage_from_tag_to_float(subscriber_change_rate)
            average_view_change_rate = self.percentage_from_tag_to_float(average_view_change_rate)
            channel_id = str(content[youtuber].find(class_='link clearfix', href=True)).strip().split(
                'href="/youtube/channel/'
            )[1].split('">')[0]

            channel_statistics = [rank,channel_name, current_subscriber, subscriber_change_rate, current_average_view,
                                  average_view_change_rate, channel_id]
            print(channel_statistics)
            ycs.append(channel_statistics)

            if youtuber + 2 >= len(content):
                break

        return ycs, document.prettify()
