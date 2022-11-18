from config.config import Config
from utils.data_format import DataFormat
from tqdm import tqdm
from collections import Counter

import os
import nltk
import pandas as pd
import string


nltk.download('all')
config = Config()
data_format = DataFormat()


def get_comments():
    youtube_comments_data = dict()
    youtube_comments_csv = dict()
    youtube_comments_filename = dict()

    for status in config.status:
        youtube_comments_data[status] = dict()
        youtube_comments_csv[status] = dict()
        youtube_comments_filename[status] = os.listdir(config.comments_csv_folder_path[status])
        for category in config.categories:
            for file in youtube_comments_filename[status]:
                if file.startswith(category):
                    youtube_comments_csv[status][category] = data_format.csv_reader(
                        os.path.join(config.comments_csv_folder_path[status], file)
                    )
                    break
            youtube_comments_data[status][category] = youtube_comments_csv[status][category][
                config.comments_header[2]].tolist()
    return youtube_comments_data


def tokenize(comments):
    tokenized_comments = dict()
    for status in config.status:
        tokenized_comments[status] = dict()
        for category in config.categories:
            tokenized_comments[status][category] = list()
            for sentence in tqdm(comments[status][category]):
                tokenized_comments[status][category].extend(nltk.tokenize.word_tokenize(str(sentence)))
    return tokenized_comments


def punctuation(comment_tokens):
    punctuation_removed_comments = dict()
    for status in config.status:
        punctuation_removed_comments[status] = dict()
        for category in config.categories:
            punctuation_removed_comments[status][category] = list()
            punctuation_removed_comments[status][category] = [
                w for w in tqdm(comment_tokens[status][category]) if w not in string.punctuation
            ]
    return punctuation_removed_comments


def english(punctuation_removed_comments):
    keep_english_only_comments = dict()
    for status in config.status:
        keep_english_only_comments[status] = dict()
        for category in config.categories:
            keep_english_only_comments[status][category] = list()
            for word in tqdm(punctuation_removed_comments[status][category]):
                if word in nltk.corpus.words.words():
                    keep_english_only_comments[status][category].extend(word)
    return keep_english_only_comments


def stopwords(keep_english_only_comments):
    stopwords_removed_comments = dict()
    for status in config.status:
        stopwords_removed_comments[status] = dict()
        for category in config.categories:
            stopwords_removed_comments[status][category] = list()
            stopwords_removed_comments[status][category] = [
                w for w in tqdm(keep_english_only_comments[status][category]) if w not in nltk.corpus.stopwords.words()
            ]
    return stopwords_removed_comments


def word_stem(stopwords_removed_comments):
    word_stem_comments = dict()
    for status in config.status:
        word_stem_comments[status] = dict()
        for category in config.categories:
            word_stem_comments[status][category] = list()
            for word in tqdm(stopwords_removed_comments[status][category]):
                word_stem_comments[status][category].extend(nltk.stem.porter.PorterStemmer.stem(word=word))
    return word_stem_comments


def word_count(word_stem_comments):
    word_counted_comments = dict()
    for status in config.status:
        word_counted_comments[status] = dict()
        for category in tqdm(config.categories):
            word_counted_comments[status][category] = dict()
            word_counted_comments[status][category] = Counter(word_stem_comments[status][category])
    return word_counted_comments


def comment_data_save(comments):
    for status in config.status:
        if not os.path.isdir(config.comments_json_folder_path[status]):
            os.makedirs(config.comments_json_folder_path[status])
        for category in config.categories:
            data_format.csv_saver(
                os.path.join(config.comments_json_folder_path[status],
                             config.csv_file_name[status][category].strip('category')[0] + '.csv'),
                config.comment_words_header,
                pd.Series(comments[status][category]).to_frame()
            )


if __name__ == '__main__':
    youtube_comments = get_comments()

    print('\n\nTOKENIZE COMMENTS\n')
    youtube_comments_tokenized = tokenize(youtube_comments)

    print('\n\nREMOVE PUNCTUATION\n')
    punctuation_removed_youtube_comments = punctuation(youtube_comments_tokenized)

    print('\n\nKEEP ENGLISH ONLY\n')
    keep_english_only_youtube_comments = english(punctuation_removed_youtube_comments)

    print('\n\nREMOVE STOPWORDS\n')
    stopwords_removed_youtube_comments = stopwords(keep_english_only_youtube_comments)

    print('\n\nWORD STEM\n')
    word_stem_youtube_comments = word_stem(stopwords_removed_youtube_comments)

    print('\n\nWORD COUNT\n')
    word_counted_youtube_comments = word_count(word_stem_youtube_comments)

    comment_data_save(word_counted_youtube_comments)

