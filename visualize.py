from utils.data_formatter import DataFormatter
from utils.visualizer import Visualizer
from config.config import Config

import os
import datetime

data_format = DataFormatter()
visualizer = Visualizer()
config = Config()


def get_comment_word_data():
    data = dict()
    csv_folder_path = None
    for p in config.vdata_period:  # all, 1week, 2week
        data[p] = dict()
        if p == config.vdata_period[0]:
            csv_folder_path = config.pdata_all_csv_folder_path
        elif p == config.vdata_period[1]:
            csv_folder_path = config.pdata_1w_csv_folder_path
        elif p == config.vdata_period[2]:
            csv_folder_path = config.pdata_2w_csv_folder_path
        else:
            print('ERROR: No such data type')
            exit(1)
        for t1 in config.pdata_type[0]:  # duplicate, no duplicate
            data[p][t1] = dict()
            for t2 in config.pdata_type[1]:  # count, ratio, z-score
                data[p][t1][t2] = dict()
                for s in config.status:
                    data[p][t1][t2][s] = dict()
                    for c in config.categories:
                        print('\n\n**********', p.upper(), t1.upper(), t2.upper(), s.upper(), c.upper(), '**********')
                        data[p][t1][t2][s][c] = list()
                        data[p][t1][t2][s][c] = data_format.csv_reader(os.path.join(
                            csv_folder_path[t1][t2][s],
                            config.csv_filename[s][c].split(datetime.date.today().strftime('_%Y'))[0] + '.csv')
                        )
    return data[config.vdata_period[0]], data[config.vdata_period[1]], data[config.vdata_period[2]]


def visualize_by_word_cloud(data, folder_path):
    for s in config.status:
        if not os.path.isdir(folder_path[s]):
            os.makedirs(folder_path[s])
        for c in config.categories:
            fn_with_p = os.path.join(folder_path[s], config.img_filename[s][c].replace('*', config.vdata_type[0]))
            visualizer.word_cloud(two_d_list_to_dict(data[s][c]), fn_with_p)
            print('WORD CLOUD SAVED:', fn_with_p)


def two_d_list_to_dict(data):
    d_d = dict()
    for i in range(len(data)):
        d_d[data[config.pdata_header[config.pdata_type[1][0]][0]][i]] = data[config.pdata_header[
            config.pdata_type[1][0]][1]][i]
    return d_d


def visualize_by_scatter_graph(data, folder_path):
    d = dict()
    for s in config.status:
        d[s] = dict()
        if not os.path.isdir(folder_path[s]):
            os.makedirs(folder_path[s])
        for c in config.categories:
            d[s][c] = get_inverse_data_count(data, s, c, 30)
            fn_with_p = os.path.join(folder_path[s], config.img_filename[s][c].replace('*', config.vdata_type[1]))
            visualizer.scatter_graph(d[s][c], s + ' ' + c, fn_with_p)
            print('SCATTER GRAPH SAVED:', fn_with_p)


def get_inverse_data_count(data, status, category, data_len):
    d = data[status][category].sort_values(by=[config.pdata_type[1][0]], ascending=False)[:data_len].copy()
    id_d, id_l = dict(), list()
    if status in config.status[0]:
        id_d = two_d_list_to_dict(data[config.status[1]][category])
    else:
        id_d = two_d_list_to_dict(data[config.status[0]][category])
    for i in range(len(d)):
        w = d.iloc[i, 0]
        if w in id_d:
            id_l.append(id_d[w])
        else:
            id_l.append(0)
    d[config.graph[1]] = id_l
    return d


def count_visualize_by_horizontal_bar_graph(data, folder_path):
    d = dict()
    for s in config.status:
        d[s] = dict()
        if not os.path.isdir(folder_path[s]):
            os.makedirs(folder_path[s])
        for c in config.categories:
            d[s][c] = get_inverse_data_count(data, s, c, 50)
            d[s][c][config.graph[1]] *= -1
            fn_with_p = os.path.join(folder_path[s], config.img_filename[s][c].replace('*', config.vdata_type[2]))
            visualizer.count_horizontal_bar_graph(d[s][c], s + ' ' + c, fn_with_p)
            print('HORIZONTAL BAR GRAPH SAVED:', fn_with_p)


def count_data(data_all, data_1week, data_2week):
    for t in config.pdata_type[0]:  # duplicate, no duplicate
        print('\n\n**********', t.upper(), '**********')

        print('\n\n**********', 'ALL DATA', '**********')
        visualize_by_word_cloud(data_all[t][config.pdata_type[1][0]],
                                config.vdata_all_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '0 WEEK - 1 WEEK', '**********')
        visualize_by_word_cloud(data_1week[t][config.pdata_type[1][0]],
                                config.vdata_1w_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '1 WEEK - 2 WEEK', '**********')
        visualize_by_word_cloud(data_2week[t][config.pdata_type[1][0]],
                                config.vdata_2w_png_folder_path[t][config.pdata_type[1][0]])

        print('\n\n**********', 'ALL DATA', '**********')
        visualize_by_scatter_graph(data_all[t][config.pdata_type[1][0]],
                                   config.vdata_all_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '0 WEEK - 1 WEEK', '**********')
        visualize_by_scatter_graph(data_1week[t][config.pdata_type[1][0]],
                                   config.vdata_1w_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '1 WEEK - 2 WEEK', '**********')
        visualize_by_scatter_graph(data_2week[t][config.pdata_type[1][0]],
                                   config.vdata_2w_png_folder_path[t][config.pdata_type[1][0]])

        print('\n\n**********', 'ALL DATA', '**********')
        count_visualize_by_horizontal_bar_graph(data_all[t][config.pdata_type[1][0]],
                                                config.vdata_all_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '0 WEEK - 1 WEEK', '**********')
        count_visualize_by_horizontal_bar_graph(data_1week[t][config.pdata_type[1][0]],
                                                config.vdata_1w_png_folder_path[t][config.pdata_type[1][0]])
        print('\n\n**********', '1 WEEK - 2 WEEK', '**********')
        count_visualize_by_horizontal_bar_graph(data_2week[t][config.pdata_type[1][0]],
                                                config.vdata_2w_png_folder_path[t][config.pdata_type[1][0]])


def ratio_visualize_by_horizontal_bar_graph(data, folder_path):
    for s in config.status:
        if not os.path.isdir(folder_path[s]):
            os.makedirs(folder_path[s])
        for c in config.categories:
            fn_with_p = os.path.join(folder_path[s], config.img_filename[s][c].replace('*', config.vdata_type[2]))
            visualizer.ratio_horizontal_bar_graph(data[s][c][:50], s + ' ' + c, fn_with_p)
            print('VERTICAL BAR GRAPH SAVED:', fn_with_p)


def ratio_data(data_all, data_1week, data_2week):
    for t in config.pdata_type[0]:
        print('\n\n**********', t.upper(), '**********')

        print('\n\n**********', 'ALL DATA', '**********')
        ratio_visualize_by_horizontal_bar_graph(data_all[t][config.pdata_type[1][1]],
                                                config.vdata_all_png_folder_path[t][config.pdata_type[1][1]])
        print('\n\n**********', '0 WEEK - 1 WEEK', '**********')
        ratio_visualize_by_horizontal_bar_graph(data_1week[t][config.pdata_type[1][1]],
                                                config.vdata_1w_png_folder_path[t][config.pdata_type[1][1]])
        print('\n\n**********', '1 WEEK - 2 WEEK', '**********')
        ratio_visualize_by_horizontal_bar_graph(data_2week[t][config.pdata_type[1][1]],
                                                config.vdata_2w_png_folder_path[t][config.pdata_type[1][1]])


def z_score_visualize_by_horizontal_bar_graph(data, folder_path):
    for s in config.status:
        if not os.path.isdir(folder_path[s]):
            os.makedirs(folder_path[s])
        for c in config.categories:
            fn_with_p = os.path.join(folder_path[s], config.img_filename[s][c].replace('*', config.vdata_type[2]))
            visualizer.z_score_horizontal_bar_graph(data[s][c][:50], s + ' ' + c, fn_with_p)
            print('VERTICAL BAR GRAPH SAVED:', fn_with_p)


def z_score_data(data_all, data_1week, data_2week):
    for t in config.pdata_type[0]:
        print('\n\n**********', t.upper(), '**********')

        print('\n\n**********', 'ALL DATA', '**********')
        z_score_visualize_by_horizontal_bar_graph(data_all[t][config.pdata_type[1][2]],
                                                  config.vdata_all_png_folder_path[t][config.pdata_type[1][2]])
        print('\n\n**********', '0 WEEK - 1 WEEK', '**********')
        z_score_visualize_by_horizontal_bar_graph(data_1week[t][config.pdata_type[1][2]],
                                                  config.vdata_1w_png_folder_path[t][config.pdata_type[1][2]])
        print('\n\n**********', '1 WEEK - 2 WEEK', '**********')
        z_score_visualize_by_horizontal_bar_graph(data_2week[t][config.pdata_type[1][2]],
                                                  config.vdata_2w_png_folder_path[t][config.pdata_type[1][2]])


if __name__ == '__main__':
    d_a, d_1w, d_2w = get_comment_word_data()

    print('\n\n**********************************************')
    print('****************** COUNT ******************')
    print('**********************************************')
    count_data(d_a, d_1w, d_2w)

    print('\n\n**********************************************')
    print('****************** RATIO ******************')
    print('**********************************************')
    ratio_data(d_a, d_1w, d_2w)

    print('\n\n**********************************************')
    print('****************** Z-SCORE ******************')
    print('**********************************************')
    z_score_data(d_a, d_1w, d_2w)

    print('\n\n\nDONE!\n')
