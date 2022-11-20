import operator

from utils.data_formatter import DataFormatter
from utils.visualizer import Visualizer
from config.config import Config

import os

data_format = DataFormatter()
visualizer = Visualizer()
config = Config()


def get_comment_word_data(csv_folder_path):
    comment_words_data = dict()
    comment_words_csv = dict()
    comment_words_filename = dict()
    for status in config.status:
        comment_words_data[status] = dict()
        comment_words_csv[status] = dict()
        comment_words_filename[status] = os.listdir(csv_folder_path[status])
        for category in config.categories:
            for file in comment_words_filename[status]:
                if file.startswith(category):
                    comment_words_csv[status][category] = data_format.csv_reader(
                        os.path.join(csv_folder_path[status], file)
                    )
                    break
            data_list = dict()
            for row in comment_words_csv[status][category].iterrows():
                data_list[row[1]['comment']] = row[1]['count']
            comment_words_data[status][category] = data_list

    comment_words_data[config.status_avg] = dict()
    for category in config.categories:
        comment_words_data[config.status_avg][category] = dict()

    for status in config.status:
        for category in config.categories:
            if status == config.status[0]:
                for key, value in comment_words_data[status][category].items():
                    comment_words_data[config.status_avg][category][key] = value
            elif status == config.status[1]:
                for key, value in comment_words_data[status][category].items():
                    if key in comment_words_data[config.status_avg][category]:
                        comment_words_data[config.status_avg][category][key] = \
                            comment_words_data[config.status_avg][category][key] - value
                    else:
                        comment_words_data[config.status_avg][category][key] = - value
    return comment_words_data


def visualize_by_word_cloud(comment_words_data, wordcloud_png_folder_path):
    print('\n\nWORD CLOUD')
    for status in config.status:
        if not os.path.isdir(wordcloud_png_folder_path[status]):
            os.makedirs(wordcloud_png_folder_path[status])
        for category in config.categories:
            print(status.upper(), category.upper())
            visualizer.word_cloud(comment_words_data[status][category],
                                  os.path.join(wordcloud_png_folder_path[status],
                                               config.image_file_name[status][category]))


def visualize_by_horizontal_bar_graph(comment_words_data, h_bar_graph_png_folder_path):
    print('\n\nHORIZONTAL BAR GRAPH')
    graph_data = dict()
    for status in config.status:
        if not os.path.isdir(h_bar_graph_png_folder_path[status]):
            os.makedirs(h_bar_graph_png_folder_path[status])
        graph_data[status] = dict()
        for category in config.categories:
            graph_data[status][category] = dict()
            graph_data[status][category][status] = dict(
                sorted(comment_words_data[status][category].items(), key=operator.itemgetter(1), reverse=True)[:30]
            )
            data_dict = dict()
            if status == config.status[0]:
                graph_data[status][category][config.status[1]] = dict()
                for key in graph_data[status][category][status].keys():
                    if key in comment_words_data[config.status[1]][category]:
                        graph_data[status][category][config.status[1]][key] = \
                            comment_words_data[config.status[1]][category][key]
                    else:
                        graph_data[status][category][config.status[1]][key] = 0
                data_dict[status] = {category:
                                         {status:
                                              {'keys':
                                                   list(graph_data[status][category][status].keys()),
                                               'values':
                                                   list(graph_data[status][category][status].values())},
                                          config.status[1]:
                                              {'keys':
                                                   list(graph_data[status][category][config.status[1]].keys()),
                                               'values':
                                                   list(graph_data[status][category][config.status[1]].values())}}}
            elif status == config.status[1]:
                graph_data[status][category][config.status[0]] = dict()
                for key in graph_data[status][category][status].keys():
                    if key in comment_words_data[config.status[0]][category]:
                        graph_data[status][category][config.status[0]][key] = \
                            comment_words_data[config.status[0]][category][key]
                    else:
                        graph_data[status][category][config.status[0]][key] = 0
                data_dict[status] = {category:
                                         {status:
                                              {'keys':
                                                   list(graph_data[status][category][status].keys()),
                                               'values':
                                                   list(graph_data[status][category][status].values())},
                                          config.status[0]:
                                              {'keys':
                                                   list(graph_data[status][category][config.status[0]].keys()),
                                               'values':
                                                   list(graph_data[status][category][config.status[0]].values())}}}
            print(status.upper(), category.upper())
            visualizer.horizontal_bar_graph(data_dict,
                                            status + ' ' + category,
                                            os.path.join(h_bar_graph_png_folder_path[status],
                                                         config.image_file_name[status][category]))


if __name__ == '__main__':
    youtube_comment_words_data = get_comment_word_data(config.comment_words_csv_folder_path)
    date_relevant_youtube_comment_words_data = get_comment_word_data(config.date_relevant_comment_words_csv_folder_path)
    visualize_by_word_cloud(youtube_comment_words_data, config.wordcloud_png_folder_path)
    visualize_by_word_cloud(date_relevant_youtube_comment_words_data, config.date_relevant_wordcloud_png_folder_path)
    visualize_by_horizontal_bar_graph(youtube_comment_words_data, config.horizontal_bar_graph_png_folder_path)
    visualize_by_horizontal_bar_graph(date_relevant_youtube_comment_words_data,
                                      config.date_relevant_horizontal_bar_graph_png_folder_path)
    print('\n\n\nDONE!\n\n\n')
