import pandas as pd
import numpy as np
import string
# from operator import itemgetter
from collections import Counter, OrderedDict

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')      #텍스트 단위로 문장 쪼개기
nltk.download('stopwords')      #불용어 처리

from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

class model:
    def __init__(self, whiskey_df:pd.DataFrame) -> None:
        self.whiskey_df = whiskey_df
        

    def normalize_text(self, raw_text) -> str:
        '''텍스트 데이터를 처리해주는 함수이다. 불용어(the, a 등)처리, 어간추출, tokenize'''
        stop_words = set(stopwords.words('english'))    #불용어들 집합

        punctuation_table = str.maketrans({key: None for key in string.punctuation})    #특수문자들 None으로 치환

        sno = SnowballStemmer('english')
        '''
        어간추출
        아래는 chatgpt의 설명 :
        SnowballStemmer('english')은 자연어 처리에서 영어 단어의 어간(stem)을 추출하기 위한 도구입니다.
        어간(stem)은 단어의 기본형으로, 단어의 접미사나 어미를 제거하여 얻어집니다. 예를 들어, "running", "runs", "ran"은 모두 "run"이라는 단어의 어간입니다.
        SnowballStemmer는 스노우볼 언어 처리 알고리즘을 사용하여 단어의 어간을 추출합니다. 이 알고리즘은 언어에 따라 다른 규칙을 적용하여 어간 추출을 수행합니다. 
        예를 들어, 영어에서는 동사의 어간 추출에 "-ing", "-ed", "-s" 등의 접미사가 사용되므로 이를 적용하여 어간을 추출합니다.
        따라서 SnowballStemmer('english')은 영어 텍스트를 처리하고 영어 단어의 어간을 추출하는 데 유용한 도구입니다.
        '''
        try:
            word_list = word_tokenize(raw_text)     #단어 토큰화
            normalized_sentence = []
            for w in word_list:
                try:
                    w = str(w)      #숫자/특수문자가 있어서 바꾸는 듯?
                    lower_case_word = str.lower(w)      #소문자로 변환
                    stemmed_word = sno.stem(lower_case_word)            #어간 추출
                    no_punctuation = stemmed_word.translate(punctuation_table)          #문자(열 아님) 치환
                    if len(no_punctuation) > 1 and no_punctuation not in stop_words:    #불용어(stop words)가 없고, 문장 길이가 1보다 길면
                        normalized_sentence.append(no_punctuation)                      #단어를 리스트에 넣음
                except:
                    continue
            return normalized_sentence
        except:
            return ''
