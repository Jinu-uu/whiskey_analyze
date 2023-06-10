import pandas as pd
import numpy as np
import ast

class preprocessing:
    def __init__(self) -> None:
        '''필요한 csv 파일 불러오기'''
        self.casktype_df = pd.read_csv('./mapping_data/mapping_casktype.csv', encoding='latin1').set_index('cask')
        self.whiskey_df = pd.read_csv('./data/whiskeybase.csv')

    def jsontodf(self, df:pd.DataFrame, target_list:list)->pd.DataFrame:
        '''ast 라이브러리를 사용해서 csv에 json형식으로 되어있는 컬럼을 바꿔주는 함수이다.'''
        for idx in range(len(df)):
            for column in target_list:
                tmp = ast.literal_eval(df[column][idx])
                df[column][idx] = tmp
        return df

    
    def get_cask(self, casks:list) -> list:
        '''casktype_df에서 casks를 찾아 반환해주는 함수이다.'''
        cask_list = []
        for cask in casks:
            try:
                cask_list += self.casktype_df.at[cask, 'description']
            except:
                pass
        return ' '.join(cask_list * 2)

    def replace_german_spanish_chars(self,text):
        '''크롤링한 사이트 특성상 독일어와 스페인어가 많기 때문에, 문자를 바꿔준다.'''
        # 독일어와 스페인어 알파벳 대응표 with chatgpt
        german_chars = {'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}
        spanish_chars = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U', 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'}

        # 문자열에서 독일어와 스페인어 알파벳을 영어 알파벳으로 대체
        for char, repl in german_chars.items():
            text = text.replace(char, repl)
        for char, repl in spanish_chars.items():
            text = text.replace(char, repl)

        return text
    
    def main(self):
        self.jsontodf(self.whiskey_df, ['review','reviewer_name','reviewer_score'])
        self.jsontodf(self.casktype_df, ['description'])

        whiskey_df_copy = self.whiskey_df.copy()

        whiskey_df_copy=whiskey_df_copy[['name','review', 'Category', 'Distillery', 'Casktype']]
        whiskey_df_copy['concat_review'] = whiskey_df_copy['review'].apply(lambda x : '  '.join(x))
        whiskey_df_copy.fillna('-', inplace=True)

        whiskey_df_copy['Casktype']=whiskey_df_copy['Casktype'].apply(self.replace_german_spanish_chars)
        whiskey_df_copy['Casktype']=whiskey_df_copy['Casktype'].apply(lambda x : x.lower().split(' '))
        whiskey_df_copy['cask_list'] = whiskey_df_copy['Casktype'].apply(self.get_cask)
        whiskey_df_copy['review_cask'] = whiskey_df_copy.apply(lambda row : row['concat_review']+' '+row['cask_list'], axis=1)
        whiskey_df_copy['review_cask']=whiskey_df_copy['review_cask'].apply(self.replace_german_spanish_chars)

        return whiskey_df_copy