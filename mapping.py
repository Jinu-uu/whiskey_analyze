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

    def cask__mapping(self) -> None:
        '''캐스크 매핑함수'''
        # 분석할 데이터
        casktype_mapping = {'Sherry': ['fruit', 'spiciness', 'smoke'], 
           'Bourbon': ['vanilla', 'sweetness', 'caramel', 'creamy'], 
           'Burgundy': ['very fruity', 'lightly sweet', 'lightly dry'], 
           'Madeira': ['spiciness', 'light fruitiness', 'sweetness', 'dryness'], 
           'Port': ['fruit', 'spiciness'], 
           'Oloroso': ['deep', 'dark', 'nutty', 'dark ripe fruits'], 
           'Pedro Ximenez': ['very sweet', 'dark fruits', 'raisins', 'syrup'], 
           'Fino': ['light fruits', 'sweetness', 'dryness', 'light wood'], 
           'Manzanilla': ['salty', 'dryness', 'sea flavours', 'fresh', 'some fruit'], 
           'Amontillado': ['sweetness', 'nutty', 'dry', 'fresh', 'acid'], 
           'Palo Cortado': ['rich', 'sweet', 'dry', 'sweet spices', 'fruits'], 
           'Sauternes': ['sweetness', 'zest', 'acidity', 'light fruits'], 
           'Bordeaux': ['strong red fruits', 'grapes (wine)', 'berries'], 
           'Tokaji': ['light fresh fruits', 'very sweet'], 
           'Ruby Port': ['very fruity', 'dark fruits', 'berries'], 
           'Barolo': ['fruits', 'tannins (bitter)', 'dried fruits', 'heavy aromas'], 
           'Chardonnay': ['lean', 'crisp', 'acidic', 'tropical fruits'], 
           'Muscat': ['floral', 'sweet', 'citrus', 'peach'], 
           'Rum': ['sweet', 'vanilla', 'fruits'], 
           'Amarone': ['tannins (bitter)', 'dry', 'raisins', 'ripe fruits'],
           'American oak':['mellow, soft, vanilla, caramel'],
           'European oak':['spicy', 'bitter', 'stong on the wood'],
           'Mizunara Oak':['sandal wood', 'coconut', 'oriental spices'],
            'oak':['vanilla', 'coffee', 'fruit']}

        # 딕셔너리를 pandas DataFrame으로 변환
        casktype_mapping = pd.DataFrame.from_dict(casktype_mapping, orient='index', columns=['Description1', 'Description2', 'Description3', 'Description4', 'Description5'])

        # cask 컬럼 추가
        casktype_mapping.insert(loc=0, column='cask', value=casktype_mapping.index)

        # description 컬럼 추가
        casktype_mapping['description'] = casktype_mapping.values.tolist()
        casktype_mapping = casktype_mapping[['cask', 'description']]

        # 결과 출력
        for i, desc in enumerate(casktype_mapping['description']):
            casktype_mapping['description'][i] = [d for d in desc if d is not None]
        casktype_mapping = casktype_mapping.reset_index().drop(columns=['index'])
        casktype_mapping = casktype_mapping.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        casktype_mapping.to_csv('./mapping_data/mapping_casktype.csv', index=False)