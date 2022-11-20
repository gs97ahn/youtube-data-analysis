from config.config import Config
from wordcloud import WordCloud

import matplotlib.pyplot as plt

config = Config()


class Visualizer:
    def word_cloud(self, data, filename_with_path):
        wc = WordCloud(background_color='white', max_words=1000)
        wc = wc.generate_from_frequencies(data)
        plt.figure(figsize=(8, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        # plt.savefig(filename_with_path)
        plt.show()

    def horizontal_bar_graph(self, data, title, filename_with_path):
        pos_y = list()
        neg_y = list()
        x = list()
        for status in config.status:
            for category in config.categories:
                if category in title and status in title:
                    x.extend(data[status][category][status]['keys'])
                    pos_y.extend(data[status][category][status]['values'])
                elif category in title and status not in title:
                    if status == config.status[0]:
                        neg_y.extend(data[config.status[1]][category][config.status[0]]['values'])
                    elif status == config.status[1]:
                        neg_y.extend(data[config.status[0]][category][config.status[1]]['values'])
                    sign_alter = list()
                    for i in neg_y:
                        sign_alter.append(-i)
                    neg_y = sign_alter
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.title(title.replace('_', ' ').capitalize())
        if config.status[0] in title:
            plt.barh(x, pos_y, label=config.status[0])
            plt.barh(x, neg_y, label=config.status[1])
        else:
            plt.barh(x, neg_y, label=config.status[0])
            plt.barh(x, pos_y, label=config.status[1])
        plt.xlabel('Frequency')
        plt.ylabel('Word')
        plt.legend()
        # plt.savefig(filename_with_path)
        plt.show()
