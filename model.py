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


    def pca_wine_variety(self, list_of_varieties, wine_attribute, whiskey_df_vecs, pca=True) -> list:
        '''subset wine vectors 메소드 호출 후 ? pca를 통해서 위스키의 맛/향/바디감을 차원축소를 한 뒤 반환'''
        wine_var_vectors = self.subset_wine_vectors(list_of_varieties, wine_attribute, whiskey_df_vecs)   #와인 이름, 벡터, 출현빈도 높은 단어
        wine_varieties = [str(w[0]).replace('(', '').replace(')', '').replace("'", '').replace('"', '') for w in wine_var_vectors]  #와인 이름의 괄호, 따옴표 처리
        wine_var_vec = [w[1] for w in wine_var_vectors]  #wine_var_vectors에서 벡터만 추출
        if pca:             #aroma 아닐 때 차원축소 하나의 값으로만
            pca = PCA(1)
            wine_var_vec = pca.fit_transform(wine_var_vec)
            wine_var_vec = pd.DataFrame(wine_var_vec, index=wine_varieties)
        else:              #aroma일 때 그냥 Series로
            wine_var_vec = pd.Series(wine_var_vec, index=wine_varieties)
        wine_var_vec.sort_index(inplace=True)
        
        wine_descriptors = pd.DataFrame([w[2] for w in wine_var_vectors], index=wine_varieties)
        wine_descriptors.sort_index(inplace=True)
            
        return wine_var_vec, wine_descriptors
    
    def normalize(self, df, cols_to_normalize) -> pd.DataFrame:
        '''df 정규화'''
        for feature_name in cols_to_normalize:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            df[feature_name] = df[feature_name].apply(lambda x: (x- min_value)/(max_value-min_value))
        return df
    
    def main(self) -> None:
        '''전처리된 whiskey_df를 향을최빈값, 바디감/맛을 1차원 값으로 변환'''
        whiskey_review_data = list(self.whiskey_df['review_cask'])      #위스키 데이터프레임의 리뷰 정보들을 list로 변환

        full_whiskey_reviews_list = [str(r) for r in whiskey_review_data]
        full_whiskey_corpus = ' '.join(full_whiskey_reviews_list)             #전체 리뷰를 str로 join
        whiskey_sentences_tokenized = sent_tokenize(full_whiskey_corpus) 
        normalized_whiskey_sentences = []
        
        for s in whiskey_sentences_tokenized:      #whiskey tokenzied : 리뷰를 센텐스로 쪼갠 데이터(list)
            normalized_text = self.normalize_text(s)
            normalized_whiskey_sentences.append(normalized_text)
        

        whiskey_bigram_model = Phrases(normalized_whiskey_sentences, min_count=100)       #함께 자주 등장하는 단어를 인식해서 묶어줌(bigram)
        whiskey_bigrams = [whiskey_bigram_model[line] for line in normalized_whiskey_sentences]  #적용
        whiskey_trigram_model = Phrases(whiskey_bigrams, min_count=50)                    #다시 묶어서 trigram 으로 만듦
        phrased_whiskey_sentences = [whiskey_trigram_model[line] for line in whiskey_bigrams]    #적용
        whiskey_trigram_model.save('whiskey_trigrams.pkl')  #모델 저장
        whiskey_trigram_model = Phraser.load('whiskey_trigrams.pkl')

        descriptor_mapping = pd.read_csv('./mapping_data/concat_descriptor_mapping.csv', encoding='latin1').set_index('raw descriptor')

        normalized_whiskey_sentences = []
        for sent in phrased_whiskey_sentences:
            normalized_whiskey_sentence = []
            for word in sent:
                normalized_word = self.return_mapped_descriptor(word, descriptor_mapping)
                normalized_whiskey_sentence.append(str(normalized_word))
            normalized_whiskey_sentences.append(normalized_whiskey_sentence)
        #이렇게 해서 만들어진 normalized_wind_sentences에는 단어별로 쪼갠것을 매핑하여 다시 문장(리스트)로 변환됨
        whiskey_reviews = list(self.whiskey_df['review_cask'])    #Description만 추출

        descriptor_mapping = pd.read_csv('./mapping_data/concat_descriptor_mapping_tastes.csv', encoding='latin1').set_index('raw descriptor')

        core_tastes = ['aroma', 'weight', 'sweet', 'acid', 'salt', 'piquant', 'fat', 'bitter']
        descriptor_mappings = dict()
        for c in core_tastes:
            #매핑 데이터를 위의 core_tastes로 분류함
            if c=='aroma':
                descriptor_mapping_filtered=descriptor_mapping.loc[descriptor_mapping['type']=='aroma']
            else:
                descriptor_mapping_filtered=descriptor_mapping.loc[descriptor_mapping['primary taste']==c]
            descriptor_mappings[c] = descriptor_mapping_filtered   


        w2v_model_list = []
        review_descriptors = []

        #word2vec를 사용하기 위해서 trigram을 사용해 미리 전처리
        for review in whiskey_reviews:
            taste_descriptors = []
            normalized_review = self.normalize_text(review)
            phrased_review = whiskey_trigram_model[normalized_review]    #trigram 모델에 넣고 반환
            
            for c in core_tastes:                                                      
                descriptors_only = [self.return_descriptor_from_mapping(descriptor_mappings[c], word, c) for word in phrased_review]
                no_nones = [str(d).strip() for d in descriptors_only if d is not None]
                descriptorized_review = ' '.join(no_nones)
                taste_descriptors.append(descriptorized_review)
            w2v_model_list.append(''.join(taste_descriptors).split(' '))
            review_descriptors.append(taste_descriptors)
        
        whiskey_word2vec_model = Word2Vec(sentences=w2v_model_list, vector_size=300, min_count=8, epochs=15)
        whiskey_word2vec_model.save('whiskey_word2vec_model.bin')
        whiskey_word2vec_model = Word2Vec.load('whiskey_word2vec_model.bin')
        #word2vec 모델을 만들고 저장
