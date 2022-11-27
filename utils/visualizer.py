from config.config import Config
from wordcloud import WordCloud

import matplotlib.pyplot as plt

config = Config()


class Visualizer:
    def word_cloud(self, data, filename_with_path):
        wc = WordCloud(background_color='white', max_words=100)
        wc = wc.generate_from_frequencies(data)
        plt.figure(figsize=(8, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(filename_with_path)
        plt.show()

    def scatter_graph(self, data, title, filename_with_path):
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        plt.title(title.replace('_', ' ').upper())
        plt.scatter(data[config.graph[0]], data[config.graph[1]])
        self.text_in_graph(data[config.graph[0]], data[config.graph[1]], data[config.graph[2]])
        if config.status[0] in title:
            plt.xlabel(config.status[0])
            plt.ylabel(config.status[1])
        else:
            plt.xlabel(config.status[1])
            plt.ylabel(config.status[0])
        plt.savefig(filename_with_path)
        plt.show()

    def text_in_graph(self, x, y, texts):
        for i in range(len(texts)):
            plt.text(x=x.iloc[i], y=y.iloc[i], s=texts.iloc[i], fontdict=dict(size=10))

    def count_horizontal_bar_graph(self, data, title, filename_with_path):
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['ytick.labelsize'] = 7
        plt.title(title.replace('_', ' ').upper())
        if config.status[0] in title:
            plt.barh(data[config.graph[2]], data[config.graph[0]], label=config.status[0])
            plt.barh(data[config.graph[2]], data[config.graph[1]], label=config.status[1])
        else:
            plt.barh(data['word'], data['count'], label=config.status[1])
            plt.barh(data['word'], data['inverse count'], label=config.status[0])
        plt.xlabel('Frequency')
        plt.ylabel('Word')
        plt.legend()
        plt.savefig(filename_with_path)
        plt.show()

    def ratio_horizontal_bar_graph(self, data, title, filename_with_path):
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['ytick.labelsize'] = 7
        plt.title(title.replace('_', ' ').upper())
        plt.barh(data[config.graph[2]], data[config.graph[3]])
        plt.xlabel('Ratio')
        plt.ylabel('Word')
        plt.savefig(filename_with_path)
        plt.show()

    def z_score_horizontal_bar_graph(self, data, title, filename_with_path):
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['ytick.labelsize'] = 7
        plt.title(title.replace('_', ' ').upper())
        plt.barh(data[config.graph[2]], data[config.graph[4]])
        plt.xlabel('Z-Score')
        plt.ylabel('Word')
        plt.savefig(filename_with_path)
        plt.show()