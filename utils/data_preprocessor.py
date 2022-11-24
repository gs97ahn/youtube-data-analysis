from tqdm import tqdm
from collections import Counter
from config.config import Config

import nltk
import string
import time
import operator
import scipy.stats as stats

config = Config()


class DataPreprocessor:
    def tokenize(self, comments, option):
        print('TOKENIZING COMMENTS')
        time.sleep(0.5)
        result = list()
        if option == config.pdata_type[0][0]:
            for sentence in tqdm(comments):
                result.extend(nltk.tokenize.word_tokenize(str(sentence)))
        elif option == config.pdata_type[0][1]:
            for sentence in tqdm(comments):
                result.extend(list(dict.fromkeys(nltk.tokenize.word_tokenize(str(sentence)))))
        else:
            print('ERROR: Option must be either "allow duplicate" or "disallow duplicate"')
        return result

    def punctuation(self, words):
        print('REMOVING PUNCTUATION')
        time.sleep(0.5)
        punctuation_set = set(string.punctuation)
        return [word for word in tqdm(words) if word not in punctuation_set]

    def english(self, words):
        print('REMOVING NON-ENGLISH WORDS')
        time.sleep(0.5)
        result = list()
        english_set = set(nltk.corpus.words.words())
        for w in tqdm(words):
            if w in english_set:
                result.append(w.lower())
        return result

    def stopwords(self, words):
        print('REMOVING STOPWORDS')
        time.sleep(0.5)
        stopwords_set = set(nltk.corpus.stopwords.words('english'))
        return [word for word in tqdm(words) if word not in stopwords_set]

    def word_stem(self, words):
        print('WORD STEM')
        time.sleep(0.5)
        stemmer = nltk.stem.porter.PorterStemmer()
        result = list()
        for word in tqdm(words):
            result.append(stemmer.stem(word))
        return result

    def word_count(self, words):
        print('COUNTING WORD')
        time.sleep(0.5)
        return Counter(words)

    def calculate_ratio(self, counts, comments_len, category):
        print('CALCULATING DATA - INVERSE DATA')
        time.sleep(0.5)
        result = dict()
        for i in tqdm(counts[config.status[0]][category]):
            result[i[0]] = i[1] / comments_len[config.status[0]][category]
        for i in tqdm(counts[config.status[1]][category]):
            if i[0] in result:
                result[i[0]] = result[i[0]] - (i[1] / comments_len[config.status[1]][category])
            else:
                result[i[0]] = -i[1]
        return result

    def calculate_z_score(self, ratios):
        print('CALCULATING Z-SCORE')
        time.sleep(0.5)
        z_scores, result = list(), list()
        for i in tqdm(ratios):
            z_scores.append(i[1])
        z_scores = stats.zscore(z_scores)
        for i in tqdm(range(len(ratios))):
            result.append([ratios[i][0], z_scores[i]])
        return result
