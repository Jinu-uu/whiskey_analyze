import pandas as pd
import numpy as np
import ast

class preprocessing:
    def __init__(self) -> None:
        '''필요한 csv 파일 불러오기'''
        self.casktype_df = pd.read_csv('./mapping_data/mapping_casktype.csv', encoding='latin1').set_index('cask')
        self.whiskey_df = pd.read_csv('./data/whiskeybase.csv')