from config.config import Config
from utils.data_format import DataFormat
from datetime import datetime
from utils.data_preprocessor import DataPreprocessor

import os
import nltk

nltk.download('all')
config = Config()
data_format = DataFormat()
data_preprocessor = DataPreprocessor()


def preprocess_comment_data():
    comment_data = dict()
    comment_csv = dict()
    comment_filename = dict()
    for status in config.status:
        comment_data[status] = dict()
        comment_csv[status] = dict()
        comment_filename[status] = os.listdir(config.comments_csv_folder_path[status])
        for category in config.categories:
            for file in comment_filename[status]:
                if file.startswith(category):
                    comment_csv[status][category] = data_format.csv_reader(
                        os.path.join(config.comments_csv_folder_path[status], file)
                    )
                    break
            comment_data[status][category] = comment_csv[status][category][config.comments_header[2]].tolist()

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
        if not os.path.isdir(config.comment_words_csv_folder_path[status]):
            os.makedirs(config.comment_words_csv_folder_path[status])
        for category in config.categories:
            data_list = []
            for key, value in word_count_comments[status][category].items():
                data_list.append([key, value])
            data_format.csv_saver(
                os.path.join(
                    config.comment_words_csv_folder_path[status],
                    config.csv_file_name[status][category].split(datetime.today().strftime('_%Y'))[0] + '.csv'
                ),
                config.comment_words_header,
                data_list
            )


if __name__ == '__main__':
    preprocess_comment_data()
    print('\n\n\nDONE!\n\n\n')

