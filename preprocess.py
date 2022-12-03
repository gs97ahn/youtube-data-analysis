from config.config import Config
from utils.data_formatter import DataFormatter
from utils.data_preprocessor import DataPreprocessor
from tqdm import tqdm

import os
import nltk
import pandas as pd
import datetime
import time

nltk.download('all')
config = Config()
data_formatter = DataFormatter()
data_preprocessor = DataPreprocessor()


def get_comment_data():
    filenames = dict()
    comments = dict()
    data_a, data_1w, data_2w = dict(), dict(), dict()
    for s in config.status:
        filenames[s] = os.listdir(config.cdata_comments_csv_folder_path[s])
        comments[s] = dict()
        data_a[s], data_1w[s], data_2w[s] = dict(), dict(), dict()
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            comments[s][c] = pd.DataFrame()
            data_a[s][c], data_1w[s][c], data_2w[s][c] = list(), list(), list()
            for f in filenames[s]:
                if f.startswith(c):
                    comments[s][c] = pd.concat([
                        comments[s][c], data_formatter.csv_reader(
                            os.path.join(config.cdata_comments_csv_folder_path[s], f)
                        )
                    ])
                    date = get_date_from_filename(f, '.csv')
                    null_error_cnt = 0
                    for r in data_formatter.csv_reader(
                            os.path.join(config.cdata_comments_csv_folder_path[s], f)
                    ).iterrows():
                        try:
                            comment_date = get_date_from_comment(r, 'T')
                        except AttributeError:
                            null_error_cnt += 1
                            continue
                        if date - comment_date < datetime.timedelta(weeks=1):
                            data_1w[s][c].append(r[1]['comment text'])
                        elif datetime.timedelta(weeks=1) <= date - comment_date < datetime.timedelta(weeks=2):
                            data_2w[s][c].append(r[1]['comment text'])
                    if null_error_cnt != 0:
                        print('ERROR: Found', null_error_cnt, 'null updated date')
            data_a[s][c].extend(comments[s][c][config.cdata_comments_header[2]].tolist())
    return [data_a, data_1w, data_2w]


def get_date_from_filename(file, split_type):
    return datetime.date(int(file.split('category_')[1].split('-')[0]),
                         int(file.split('category_')[1].split('-')[1]),
                         int(file.split('category_')[1].split('-')[2].strip(split_type)))


def get_date_from_comment(comment, split_type):
    return datetime.date(int(comment[1]['updated at'].split('-')[0]),
                         int(comment[1]['updated at'].split('-')[1]),
                         int(comment[1]['updated at'].split('-')[2].split(split_type)[0]))


def count(comments, token_function_option):
    data, result = dict(), dict()
    for s in config.status:
        data[s], result[s] = dict(), dict()
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            data[s][c] = count_cycle(comments[s][c], token_function_option)
            result[s][c] = dict_to_2d_list(data[s][c])
    return result


def dict_to_2d_list(dict_data):
    result = list()
    for key, value in dict_data.items():
        result.append([key, value])
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def count_cycle(data, token_function_option):
    data = data_preprocessor.tokenize(data, token_function_option, True)
    data = data_preprocessor.punctuation(data, True)
    data = data_preprocessor.english(data, True)
    data = data_preprocessor.stopwords(data, True)
    data = data_preprocessor.word_stem(data, True)
    data = data_preprocessor.word_count(data, True)
    return data


def ratio(counts, data_len):
    r_data, result = dict(), dict()
    for s in config.status:
        r_data[s], result[s] = dict(), dict()
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            if s == config.status[0]:
                r_data[s][c] = data_preprocessor.calculate_ratio(counts, data_len, c)
            elif s == config.status[1]:
                r_data[s][c] = flip_sign(r_data[config.status[0]][c])
            result[s][c] = dict_to_2d_list(r_data[s][c])
    return result


def flip_sign(dict_data):
    time.sleep(0.5)
    f_data = dict()
    for key, value in tqdm(dict_data.items()):
        f_data[key] = -value
    return f_data


def z_score(ratios):
    result = dict()
    for s in config.status:
        result[s] = dict()
        for c in config.categories:
            print('\n\n**********', s.upper(), c.upper(), '**********')
            result[s][c] = data_preprocessor.calculate_z_score(ratios[s][c])
    return result


def data_length(comment):
    data_len = dict()
    for s in config.status:
        data_len[s] = dict()
        for c in config.categories:
            data_len[s][c] = len(comment)
    return data_len


def save_data_file(data, csv_folder_path, header_option):
    header = None
    if header_option == config.pdata_type[1][0]:
        header = config.pdata_header[config.pdata_type[1][0]]
    elif header_option == config.pdata_type[1][1]:
        header = config.pdata_header[config.pdata_type[1][1]]
    elif header_option == config.pdata_type[1][2]:
        header = config.pdata_header[config.pdata_type[1][2]]
    else:
        print('ERROR: Unknown header option -', header_option)
        exit(1)
    for s in config.status:
        if not os.path.isdir(csv_folder_path[s]):
            os.makedirs(csv_folder_path[s])
        for c in config.categories:
            data_formatter.csv_saver(
                os.path.join(csv_folder_path[s],
                             config.csv_filename[s][c].split(datetime.date.today().strftime('_%Y'))[0] + '.csv'),
                header,
                data[s][c]
            )


if __name__ == '__main__':
    d_list = get_comment_data()
    f_path = None
    for i in range(len(d_list)):
        if i == 0:
            f_path = config.pdata_all_csv_folder_path
            d_type = 'ALL DATA'
        elif i == 1:
            f_path = config.pdata_1w_csv_folder_path
            d_type = '0 WEEK - 1 WEEK'
        else:
            f_path = config.pdata_2w_csv_folder_path
            d_type = '1 WEEK - 2 WEEK'

        data_len_list = data_length(d_list[i])

        for dup_opt in config.pdata_type[0]:
            print('\n\n**********************************************')
            print('**********************************************')
            print('**********', d_type, dup_opt.upper(), config.pdata_type[1][0].upper(), '**********')
            print('**********************************************')
            print('**********************************************')
            d_c = count(d_list[i], dup_opt)
            save_data_file(d_c, f_path[dup_opt][config.pdata_type[1][0]], config.pdata_type[1][0])
            d_r = ratio(d_c, data_len_list)
            save_data_file(d_r, f_path[dup_opt][config.pdata_type[1][1]], config.pdata_type[1][1])
            d_z = z_score(d_r)
            save_data_file(d_z, f_path[dup_opt][config.pdata_type[1][2]], config.pdata_type[1][2])

    print('\n\n\nDONE!\n')
