from tqdm import tqdm
from collections import Counter

import nltk
import string
import time


class DataPreprocessor:
    def tokenize(comments):
        print('\nTOKENIZE COMMENTS\n')
        time.sleep(0.1)
        tokenized_comments = list()
        for sentence in tqdm(comments):
            tokenized_comments.extend(nltk.tokenize.word_tokenize(str(sentence)))
        return tokenized_comments

    def punctuation(words):
        print('\nREMOVE PUNCTUATION\n')
        time.sleep(0.1)
        return [word for word in tqdm(words) if word not in string.punctuation]

    def english(words):
        print('\nKEEP ENGLISH ONLY\n')
        time.sleep(0.1)
        keep_english_only_words = list()
        for word in tqdm(words):
            if word in nltk.corpus.words.words():
                keep_english_only_words.append(word.lower())
        return keep_english_only_words

    def stopwords(words):
        print('\nREMOVE STOPWORDS\n')
        time.sleep(0.1)
        return [word for word in tqdm(words) if word not in nltk.corpus.stopwords.words('english')]

    def word_stem(words):
        print('\nWORD STEM\n')
        time.sleep(0.1)
        stemmer = nltk.stem.porter.PorterStemmer()
        word_stem_words = list()
        for word in tqdm(words):
            word_stem_words.append(stemmer.stem(word))
        return word_stem_words

    def word_count(words):
        print('\nWORD COUNT\n')
        time.sleep(0.1)
        return Counter(words)