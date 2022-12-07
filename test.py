from config.config import Config
from utils.data_formatter import DataFormatter
from utils.data_preprocessor import DataPreprocessor
from tqdm import tqdm

import os
import datetime

config = Config()
data_formatter = DataFormatter()
data_preprocessor = DataPreprocessor()


def get_test_data_date():
    filenames, dates = dict(), dict()
    for s in config.status:
        dates[s] = dict()
        filenames[s] = os.listdir(config.cdata_videos_and_video_statistics_csv_folder_path[s])
        filenames[s].sort(reverse=True)
        for c in config.categories:
            dates[s][c] = list()
            for f in filenames[s]:
                if f.__contains__(c):
                    print(f)
                    dates[s][c] = (datetime.date(int(f.split('category_')[1].split('-')[0]),
                                                int(f.split('category_')[1].split('-')[1]),
                                                int(f.split('category_')[1].split('-')[2].strip('.csv'))))
                    break
    return dates


def get_test_channel_data():
    print('\n\n********** GETTING TEST CHANNEL DATA **********')
    filenames, test_data = dict(), dict()
    for s in config.status:
        test_data[s] = dict()
        filenames[s] = os.listdir(config.cdata_videos_and_video_statistics_csv_folder_path[s])
        filenames[s].sort(reverse=True)
        for c in config.categories:
            test_data[s][c] = dict()
            data = None
            for f in filenames[s]:
                if f.__contains__(c):
                    data = data_formatter.csv_reader(config.cdata_videos_and_video_statistics_csv_folder_path[s] + f)
                    break
            for cid, vid in zip(data[config.cdata_videos_and_video_statistics_header[0]],
                                data[config.cdata_videos_and_video_statistics_header[1]]):
                test_data[s][c][vid] = cid
    return test_data


def get_test_comment_data():
    print('\n\n********** GETTING TEST COMMENT DATA **********')
    filenames, test_data = dict(), dict()
    for s in config.status:
        test_data[s] = dict()
        filenames[s] = os.listdir(config.cdata_comments_csv_folder_path[s])
        filenames[s].sort(reverse=True)
        for c in config.categories:
            for f in filenames[s]:
                if f.__contains__(c):
                    test_data[s][c] = data_formatter.csv_reader(config.cdata_comments_csv_folder_path[s] + f)
                    break
    return test_data


def get_preprocessed_data(data_folder_path, pdata_header):
    print('\n\n********** GETTING PREPROCESSED DATA **********')
    pdata_filenames, pdata = dict(), dict()
    for s in config.status:
        pdata_filenames[s], pdata[s] = dict(), dict()
        filenames = os.listdir(data_folder_path[s])
        for c in config.categories:
            pdata_filenames[s][c], pdata[s][c] = str(), dict()
            for f in filenames:
                if f.__contains__(c):
                    pdata_filenames[s][c] = data_formatter.csv_reader(data_folder_path[s] + f)
                    break
            for w, r in zip(pdata_filenames[s][c][pdata_header[0]], pdata_filenames[s][c][pdata_header[1]]):
                pdata[s][c][w] = r
    return pdata


def extract_test_data(test_channel_data, test_comment_data, token_function_option, dates):
    print('\n\n********** EXTRACTING TEST DATA **********')
    all_channel_comments, w1_channel_comments, w2_channel_comments = dict(), dict(), dict()
    for s in config.status:
        all_channel_comments[s], w1_channel_comments[s], w2_channel_comments[s] = dict(), dict(), dict()
        for c in config.categories:
            all_channel_comments[s][c], w1_channel_comments[s][c], w2_channel_comments[s][c] = list(), list(), list()
            current_channel = ''
            all_current_comments, w1_current_comments, w2_current_comments = list(), list(), list()
            for i in tqdm(range(len(test_comment_data[s][c]))):
                vid = test_comment_data[s][c][config.cdata_comments_header[0]][i]
                com = str(test_comment_data[s][c][config.cdata_comments_header[2]][i])
                dat = test_comment_data[s][c][config.cdata_comments_header[4]][i]
                cid = test_channel_data[s][c][vid]
                try:
                    comment_date = get_comment_date(dat)
                except AttributeError:
                    continue
                if cid == current_channel:
                    words = cycle(com.lower(), token_function_option)
                    all_current_comments.extend(words)
                else:
                    current_channel = cid
                    if len(all_current_comments) != 0:
                        all_channel_comments[s][c].append(all_current_comments.copy())
                        w1_channel_comments[s][c].append(w1_current_comments.copy())
                        w2_channel_comments[s][c].append(w2_current_comments.copy())
                    all_current_comments.clear()
                    w1_current_comments.clear()
                    w2_current_comments.clear()
                    words = cycle(com.lower(), token_function_option)
                    all_current_comments.extend(words)
                if dates[s][c] - comment_date < datetime.timedelta(weeks=1):
                    w1_current_comments.extend(words)
                elif datetime.timedelta(weeks=1) <= dates[s][c] - comment_date < datetime.timedelta(weeks=2):
                    w2_current_comments.extend(words)
    return all_channel_comments, w1_channel_comments, w2_channel_comments


def get_comment_date(date):
    return datetime.date(int(date.split('-')[0]),
                         int(date.split('-')[1]),
                         int(date.split('-')[2].split('T')[0]))


def cycle(comment, token_function_option):
    comment = data_preprocessor.tokenize(comment, token_function_option, False)
    comment = data_preprocessor.punctuation(comment, False)
    comment = data_preprocessor.english(comment, False)
    comment = data_preprocessor.stopwords(comment, False)
    comment = data_preprocessor.word_stem(comment, False)
    return comment


def find_model_accuracy(model, test_data):
    print('\n\n********** FINDING MODEL ACCURACY **********')
    accuracy = dict()
    for s in config.status:
        accuracy[s] = dict()
        for c in config.categories:
            print(s.upper(), c.upper())
            accuracy[s][c] = list()
            for i in tqdm(range(len(test_data[s][c]))):
                accuracy[s][c].append(0)
                for w in test_data[s][c][i]:
                    if w in set(model[s][c].keys()):
                        accuracy[s][c][i] += model[s][c][w]
                    else:
                        continue

    return accuracy


def find_model_total_category_accuracy(accuracy):
    print('\n\n********** FINDING MODEL TOTAL CATEGORY ACCURACY **********')
    total_accuracy = dict()
    for c in config.categories:
        print(c.upper())
        total_accuracy[c] = 0
        for s in config.status:
            for a in accuracy[s][c]:
                if a > 0:
                    total_accuracy[c] += 1
                else:
                    continue
        print(total_accuracy[c], '/ (', (len(accuracy[config.status[0]][c]), '+', len(accuracy[config.status[1]][c]), ')'))
        total_accuracy[c] = total_accuracy[c] / (len(accuracy[config.status[0]][c]) + len(accuracy[config.status[1]][c]))
    return total_accuracy


def print_accuracy(accuracy):
    for c in config.categories:
        print(c + ':', accuracy[c])


if __name__ == '__main__':
    test_dates = get_test_data_date()
    test_channel_d = get_test_channel_data()
    test_comment_d = get_test_comment_data()
    all_test_dup_d, w1_test_dup_d, w2_test_dup_d = extract_test_data(test_channel_d, test_comment_d,
                                                                    config.pdata_type[0][0], test_dates)
    all_test_nodup_d, w1_test_nodup_d, w2_test_nodup_d = extract_test_data(test_channel_d, test_comment_d,
                                                                          config.pdata_type[0][1], test_dates)

    # # Testing with RATIO
    # All Duplicate
    all_dup_ratio = get_preprocessed_data(
        config.pdata_all_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    a_d_r_acc = find_model_accuracy(all_dup_ratio, all_test_dup_d)
    a_d_r_tot_acc = find_model_total_category_accuracy(a_d_r_acc)

    # All No Duplicate
    all_nodup_ratio = get_preprocessed_data(
        config.pdata_all_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    a_nd_r_acc = find_model_accuracy(all_nodup_ratio, all_test_nodup_d)
    a_nd_r_tot_acc = find_model_total_category_accuracy(a_nd_r_acc)

    # 1 Week Duplicate
    w1_dup_ratio = get_preprocessed_data(
        config.pdata_1w_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    w1_d_r_acc = find_model_accuracy(w1_dup_ratio, w1_test_dup_d)
    w1_d_r_tot_acc = find_model_total_category_accuracy(w1_d_r_acc)

    # 1 Week No Duplicate
    w1_nodup_ratio = get_preprocessed_data(
        config.pdata_1w_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    w1_nd_r_acc = find_model_accuracy(w1_nodup_ratio, w1_test_nodup_d)
    w1_nd_r_tot_acc = find_model_total_category_accuracy(w1_nd_r_acc)

    # 2 Week Duplicate
    w2_dup_ratio = get_preprocessed_data(
        config.pdata_2w_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    w2_d_r_acc = find_model_accuracy(w2_dup_ratio, w2_test_dup_d)
    w2_d_r_tot_acc = find_model_total_category_accuracy(w2_d_r_acc)

    # 2 Week No Duplicate
    w2_nodup_ratio = get_preprocessed_data(
        config.pdata_2w_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][1]],
        config.pdata_header[config.pdata_type[1][1]]
    )
    w2_nd_r_acc = find_model_accuracy(w2_nodup_ratio, w2_test_nodup_d)
    w2_nd_r_tot_acc = find_model_total_category_accuracy(w2_nd_r_acc)

    # # Testing with Z-SCORE
    # All Duplicate
    all_dup_zscore = get_preprocessed_data(
        config.pdata_all_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    a_d_z_acc = find_model_accuracy(all_dup_zscore, all_test_dup_d)
    a_d_z_tot_acc = find_model_total_category_accuracy(a_d_z_acc)

    # All No Duplicate
    all_nodup_zscore = get_preprocessed_data(
        config.pdata_all_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    a_nd_z_acc = find_model_accuracy(all_nodup_zscore, all_test_nodup_d)
    a_nd_z_tot_acc = find_model_total_category_accuracy(a_nd_z_acc)

    # 1 Week Duplicate
    w1_dup_zscore = get_preprocessed_data(
        config.pdata_1w_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    w1_d_z_acc = find_model_accuracy(w1_dup_zscore, w1_test_dup_d)
    w1_d_z_tot_acc = find_model_total_category_accuracy(w1_d_z_acc)

    # 1 Week No Duplicate
    w1_nodup_zscore = get_preprocessed_data(
        config.pdata_1w_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    w1_nd_z_acc = find_model_accuracy(w1_nodup_zscore, w1_test_nodup_d)
    w1_nd_z_tot_acc = find_model_total_category_accuracy(w1_nd_z_acc)

    # 2 Week Duplicate
    w2_dup_zscore = get_preprocessed_data(
        config.pdata_2w_csv_folder_path[config.pdata_type[0][0]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    w2_d_z_acc = find_model_accuracy(w2_dup_zscore, w2_test_dup_d)
    w2_d_z_tot_acc = find_model_total_category_accuracy(w2_d_z_acc)

    # 2 Week No Duplicate
    w2_nodup_zscore = get_preprocessed_data(
        config.pdata_2w_csv_folder_path[config.pdata_type[0][1]][config.pdata_type[1][2]],
        config.pdata_header[config.pdata_type[1][2]]
    )
    w2_nd_z_acc = find_model_accuracy(w2_nodup_zscore, w2_test_nodup_d)
    w2_nd_z_tot_acc = find_model_total_category_accuracy(w2_nd_z_acc)

    print('\n\n**********************************************')
    print('*************** RATIO ***************')
    print('**********************************************')
    print('\n\n********** ALL DUPLICATE **********')
    print_accuracy(a_d_r_tot_acc)
    print('\n\n********** ALL NO DUPLICATE **********')
    print_accuracy(a_nd_r_tot_acc)
    print('\n\n********** 1 WEEK DUPLICATE **********')
    print_accuracy(w1_d_r_tot_acc)
    print('\n\n********** 1 WEEK NO DUPLICATE **********')
    print_accuracy(w1_nd_r_tot_acc)
    print('\n\n********** 2 WEEK DUPLICATE **********')
    print_accuracy(w2_d_r_tot_acc)
    print('\n\n********** 2 WEEK NO DUPLICATE **********')
    print_accuracy(w2_nd_r_tot_acc)

    print('\n\n**********************************************')
    print('*************** Z-SCORE ***************')
    print('**********************************************')
    print('\n\n********** ALL DUPLICATE **********')
    print_accuracy(a_d_z_tot_acc)
    print('\n\n********** ALL NO DUPLICATE **********')
    print_accuracy(a_nd_z_tot_acc)
    print('\n\n********** 1 WEEK DUPLICATE **********')
    print_accuracy(w1_d_z_tot_acc)
    print('\n\n********** 1 WEEK NO DUPLICATE **********')
    print_accuracy(w1_nd_z_tot_acc)
    print('\n\n********** 2 WEEK DUPLICATE **********')
    print_accuracy(w2_d_z_tot_acc)
    print('\n\n********** 2 WEEK NO DUPLICATE **********')
    print_accuracy(w2_nd_z_tot_acc)
