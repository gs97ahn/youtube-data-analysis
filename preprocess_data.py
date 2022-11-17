from config.config import Config
from utils.data_format import DataFormat
from string import punctuation
from nltk.corpus import stopwords
from tqdm import tqdm

import os
import nltk


nltk.download('punkt')
config = Config()
data_format = DataFormat()


def get_comments():
    youtube_comments = dict()
    youtube_comments_csv = dict()
    youtube_comments_filename = dict()

    for status in config.status:
        youtube_comments[status] = dict()
        youtube_comments_csv[status] = dict()
        youtube_comments_filename[status] = os.listdir(config.comments_csv_folder_path[status])
        for category in config.categories:
            for file in youtube_comments_filename[status]:
                if file.startswith(category):
                    youtube_comments_csv[status][category] = data_format.csv_reader(
                        os.path.join(config.comments_csv_folder_path[status], file)
                    )
                    break
            youtube_comments[status][category] = youtube_comments_csv[status][category][
                config.comments_header[2]].tolist()
    return youtube_comments


def tokenize(comments):
    tokenized_comments = dict()
    for status in config.status:
        tokenized_comments[status] = dict()
        for category in config.categories:
            tokenized_comments[status][category] = list()
            for sentence in tqdm(comments[status][category]):
                tokenized_comments[status][category].extend(nltk.tokenize.word_tokenize(str(sentence)))
    return tokenized_comments


def punctuation_and_stop_words(comment_tokens):
    p_and_s_removed_comments = dict()
    for status in config.status:
        p_and_s_removed_comments[status] = dict()
        for category in config.categories:
            p_and_s_removed_comments[status][category] = list()
            p_and_s_removed_comments[status][category] = [
                w for w in tqdm(comment_tokens[status][category]) if w not in punctuation or stopwords.words()
            ]
    return p_and_s_removed_comments


def alphabets(punctuation_and_stop_words_removed_comments):
    keep_alphabets_only_comments = dict()
    for status in config.status:
        keep_alphabets_only_comments[status] = dict()
        for category in config.categories:
            keep_alphabets_only_comments[status][category] = list()
            for word in tqdm(punctuation_and_stop_words_removed_comments[status][category]):
                if word.isalpha():
                    keep_alphabets_only_comments[status][category].append(word)
    return keep_alphabets_only_comments


if __name__ == '__main__':
    youtube_comments = get_comments()

    print('\n\nTOKENIZE COMMENTS\n')
    youtube_comments_tokenized = tokenize(youtube_comments)

    print('\n\nREMOVE PUNCTUATION AND STOP WORDS\n')
    punctuation_and_stop_words_removed_youtube_comments = punctuation_and_stop_words(youtube_comments_tokenized)
