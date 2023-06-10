import pandas as pd
import numpy as np
import os

class mapping:
    def __init__(self)->None:
        pass

    def folder_detect(self, folder_name) -> None:
        '''해당 폴더 이름이 존재하는지, 존재하면 함수 종료, 존재하지 않으면 그 폴더 생성'''
        if not os.path.exists('./data'):   
            os.mkdir(folder_name)
    
    def distillery_mapping(self) -> None:
        '''증류소 매핑함수'''
        distillery_mapping = {
        'Distillery': ['Macallan','Springbank','Bowmore','Ardbeg','Glenfarclas',
                    'Glen Grant','Mortlach','Glendronach','Glenglassaugh','Laphroaig',
                    'Highland Park','Port Ellen','Brora','Longmorn','Dalmore',
                    'Caol Ila','Glen Garioch','Talisker','Karuizawa','Clynelish',
                    'Tobermory','Glenrothes','Glen Moray','Strathisla','Tullibardine',
                    'Linkwood','Glenlivet','Balvenie','Lagavulin','Glengoyne',
                    'Bunnahabhain','Auchentoshan','Ben Nevis','Glenugie','Glenfiddich',
                    'Caperdonich','Bruichladdich','St. Magdalene','Glen Ord','Glenury Royal',
                    'Glenburgie','Glenlochy','Tormore','Aultmore','Dailuaine',
                    'Isle of Jura','Midleton (1975-)','Miltonduff','Benromach','Fettercairn',
                    'BenRiach'],
        'Country': ['Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Japan', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Scotland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland', 'Ireland', 'Scotland', 'Scotland', 'Scotland',
                    'Scotland',]
        }
        distillery_mapping = pd.DataFrame(distillery_mapping)
        distillery_mapping.to_csv('./mapping_data/mapping_country.csv', index=False)