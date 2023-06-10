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
    
    def return_mapped_descriptor(self, word, mapping) -> str:
        '''매핑된 csv를 사용하여 정규화하는 함수.'''
        if word in list(mapping.index):
            normalized_word = mapping.at[word, 'level_3']
            return normalized_word
        else:
            return word
    
    def return_descriptor_from_mapping(self, descriptor_mapping, word, core_taste) -> str:
        '''입력 받은 단어 word가 매핑 데이터에 있으면 해당 단어의 combined 반환, 아니면 none을 반환해주는 함수'''
        if word in list(descriptor_mapping.index):
            descriptor_to_return = descriptor_mapping['combined'][word]
            return descriptor_to_return
        else:
            return None
        
    def subset_wine_vectors(self, list_of_varieties, wine_attribute, whiskey_df_vecs) -> list:
        '''맛/향/바디감을 input으로 받으면 해당하는 맛/향/바디감을 [맛/향/바디감, 벡터, 최빈값]으로 반환'''
        '''list_of_varieties - normalized_geos(와인 위치 정보 정규화한 데이터)
            wine_attribute - aroma, bitter 등 taste
            [이름, 300길이의 벡터, 2개 이상 중복된 단어 출력]
            '''
        wine_variety_vectors = []
        for v in list_of_varieties:              #list of varieties에서 loc을 사용해서 Variety, location에 맞는 열 추출
            one_var_only = whiskey_df_vecs.loc[(whiskey_df_vecs['name'] == v[0]) & 
                                                    (whiskey_df_vecs['Distillery'] == v[1])]
            if len(list(one_var_only.index)) < 1 or str(v[1][-1]) == '0':   #정보 없으면 컨티뉴
                continue
            else:
                taste_vecs = list(one_var_only[wine_attribute])      #해당 taste 리스트화
                taste_vecs = [self.avg_taste_vecs[wine_attribute] if 'numpy' not in str(type(x)) else x for x in taste_vecs]#numpy 가 아니면 avg_taste_vecs[wine_attribute], 맞으면 x
                average_variety_vec = np.average(taste_vecs, axis=0)
                descriptor_colname = wine_attribute + '_descriptors'
                all_descriptors = [item for items in list(one_var_only[descriptor_colname]) for item in items]
                word_freqs = Counter(all_descriptors)
                most_common_words = word_freqs.most_common(50)   #최빈값 50개
                top_n_words = [(i[0], "{:.2f}".format(i[1]/len(taste_vecs))) for i in most_common_words]  #most_common_word의 i[0]과 i[1]을 taste_vec의 길이로 나눈 값을 저장?
                top_n_words = [i for i in top_n_words if len(i[0])>=1]     #출현 빈도 낮은거 거르기
                wine_variety_vector = [v, average_variety_vec, top_n_words]
                    
                wine_variety_vectors.append(wine_variety_vector)
                
        return wine_variety_vectors
