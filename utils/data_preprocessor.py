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
    def tokenize(self, comments, function_option, tqdm_option):
        result = list()
        if function_option == config.pdata_type[0][0]:
            if tqdm_option:
                time.sleep(0.1)
                print('TOKENIZING COMMENTS')
                time.sleep(0.1)
                for sentence in tqdm(comments):
                    result.extend(nltk.tokenize.word_tokenize(str(sentence)))
            else:
                result.extend(nltk.tokenize.word_tokenize(str(comments).lower()))
        elif function_option == config.pdata_type[0][1]:
            if tqdm_option:
                time.sleep(0.1)
                print('TOKENIZING COMMENTS')
                time.sleep(0.1)
                for sentence in tqdm(comments):
                    result.extend(list(dict.fromkeys(nltk.tokenize.word_tokenize(str(sentence)))))
            else:
                result.extend(nltk.tokenize.word_tokenize(str(comments).lower()))
        else:
            print('ERROR: Option must be either "allow duplicate" or "disallow duplicate"')
        return result

    def punctuation(self, words, tqdm_option):
        punctuation_set = set(string.punctuation)
        if tqdm_option:
            time.sleep(0.1)
            print('REMOVING PUNCTUATION')
            time.sleep(0.1)
            return [word for word in tqdm(words) if word not in punctuation_set]
        else:
            return [word for word in words if word not in punctuation_set]

    def english(self, words, tqdm_option):
        result = list()
        english_set = set(nltk.corpus.words.words())
        if tqdm_option:
            time.sleep(0.1)
            print('REMOVING NON-ENGLISH WORDS')
            time.sleep(0.1)
            for w in tqdm(words):
                if w in english_set:
                    result.append(w.lower())
        else:
            for w in words:
                if w in english_set:
                    result.append(w.lower())
        return result

    def stopwords(self, words, tqdm_option):
        stopwords_set = set(nltk.corpus.stopwords.words('english'))
        if tqdm_option:
            time.sleep(0.1)
            print('REMOVING STOPWORDS')
            time.sleep(0.1)
            return [word for word in tqdm(words) if word not in stopwords_set]
        else:
            return [word for word in words if word not in stopwords_set]

    def word_stem(self, words, tqdm_option):
        stemmer = nltk.stem.porter.PorterStemmer()
        result = list()
        if tqdm_option:
            time.sleep(0.1)
            print('WORD STEM')
            time.sleep(0.1)
            for word in tqdm(words):
                result.append(stemmer.stem(word))
        else:
            for word in words:
                result.append(stemmer.stem(word))
        return result

    def word_count(self, words):
        time.sleep(0.1)
        print('COUNTING WORD')
        time.sleep(0.1)
        return Counter(words)

    def calculate_ratio(self, counts, comments_len, category):
        time.sleep(0.1)
        print('CALCULATING DATA - INVERSE DATA')
        time.sleep(0.1)
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
        time.sleep(0.1)
        print('CALCULATING Z-SCORE')
        time.sleep(0.1)
        z_scores, result = list(), list()
        for i in tqdm(ratios):
            z_scores.append(i[1])
        z_scores = stats.zscore(z_scores)
        for i in tqdm(range(len(ratios))):
            result.append([ratios[i][0], z_scores[i]])
        return result
