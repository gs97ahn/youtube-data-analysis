from config.config import Config
from utils.data_formatter import DataFormatter
from datetime import datetime
from utils.data_preprocessor import DataPreprocessor

import os
import nltk
import pandas as pd
import datetime

nltk.download('all')
config = Config()
data_format = DataFormatter()
data_preprocessor = DataPreprocessor()


def get_comment_data():
    comment_data = dict()
    comment_csv = dict()
    comment_filename = dict()
    date_relevant_comment_data = dict()
    for status in config.status:
        comment_data[status] = dict()
        comment_csv[status] = dict()
        date_relevant_comment_data[status] = dict()
        comment_filename[status] = os.listdir(config.comments_csv_folder_path[status])
        for category in config.categories:
            print(status.upper(), category.upper())
            comment_csv[status][category] = pd.DataFrame()
            comment_data[status][category] = list()
            date_relevant_comment_data[status][category] = list()
            for file in comment_filename[status]:
                if file.startswith(category):
                    comment_csv[status][category] = pd.concat([
                        comment_csv[status][category],
                        data_format.csv_reader(
                            os.path.join(config.comments_csv_folder_path[status], file)
                         )
                    ])
                    date = datetime.date(int(file.split('category_')[1].split('-')[0]),
                                         int(file.split('category_')[1].split('-')[1]),
                                         int(file.split('category_')[1].split('-')[2].strip('.csv')))
                    for row in data_format.csv_reader(
                            os.path.join(config.comments_csv_folder_path[status], file)
                    ).iterrows():
                        try:
                            comment_date = datetime.date(int(row[1]['updated at'].split('-')[0]),
                                                         int(row[1]['updated at'].split('-')[1]),
                                                         int(row[1]['updated at'].split('-')[2].split('T')[0]))
                        except AttributeError as e:
                            print('ERROR: Updated date is null')
                            continue
                        if date - comment_date < datetime.timedelta(weeks=1):
                            date_relevant_comment_data[status][category].append(row[1]['comment text'])
            comment_data[status][category].extend(comment_csv[status][category][config.comments_header[2]].tolist())
    return comment_data, date_relevant_comment_data


def preprocess_comment_data(comment_data, csv_folder_path):
    tokenized_comments = dict()
    punctuation_removed_comments = dict()
    keep_english_only_comments = dict()
    stopwords_removed_comments = dict()
    word_stem_comments = dict()
    word_count_comments = dict()
    for status in config.status:
        tokenized_comments[status] = dict()
        punctuation_removed_comments[status] = dict()
        keep_english_only_comments[status] = dict()
        stopwords_removed_comments[status] = dict()
        word_stem_comments[status] = dict()
        word_count_comments[status] = dict()
        for category in config.categories:
            print('\n', status.upper(), category.upper(), '\n')
            tokenized_comments[status][category] = DataPreprocessor.tokenize(comment_data[status][category])
            punctuation_removed_comments[status][category] = DataPreprocessor.punctuation(
                tokenized_comments[status][category]
            )
            keep_english_only_comments[status][category] = DataPreprocessor.english(
                punctuation_removed_comments[status][category]
            )
            stopwords_removed_comments[status][category] = DataPreprocessor.stopwords(
                keep_english_only_comments[status][category]
            )
            word_stem_comments[status][category] = DataPreprocessor.word_stem(
                stopwords_removed_comments[status][category]
            )
            word_count_comments[status][category] = DataPreprocessor.word_count(word_stem_comments[status][category])

    for status in config.status:
        if not os.path.isdir(csv_folder_path[status]):
            os.makedirs(csv_folder_path[status])
        for category in config.categories:
            data_list = []
            for key, value in word_count_comments[status][category].items():
                data_list.append([key, value])
            data_format.csv_saver(
                os.path.join(
                    csv_folder_path[status],
                    config.csv_file_name[status][category].split(datetime.date.today().strftime('_%Y'))[0] + '.csv'
                ),
                config.comment_words_header,
                data_list
            )


if __name__ == '__main__':
    youtube_comment_data, date_relevant_youtube_comment_data = get_comment_data()
    preprocess_comment_data(youtube_comment_data, config.comment_words_csv_folder_path)
    preprocess_comment_data(date_relevant_youtube_comment_data, config.date_relevant_comment_words_csv_folder_path)
    print('\n\n\nDONE!\n\n\n')
