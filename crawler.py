from lib2to3.pgen2 import driver
from typing import Union
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchWindowException
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import os
import ast

class crawler:
    def __init__(self) -> None:        
        '''크롤링에 필요한 세팅'''
        service = ChromeService(ChromeDriverManager().install())
        self.driver = ChromeDriver(service=service)

    def folder_detect(self, folder_name) -> None:
        '''해당 폴더 이름이 존재하는지, 존재하면 함수 종료, 존재하지 않으면 그 폴더 생성'''
        if not os.path.exists('./data'):   
            os.mkdir(folder_name)

    def whisky_base_crawler(self)->None:
        '''whisky base 사이트 크롤링'''
        self.folder_detect('./data')

        #먼저 whisky base 사이트의 상위 1000개 위스키 url 크롤링
        self.driver.get("https://www.whiskybase.com/whiskies/top1000")
        whiskey_top1000 = self.driver.find_elements(By.XPATH, '//tbody//tr//a[@class="clickable"]')
        url_list = [whiskey_top1000[x].get_attribute('href') for x in range(len(whiskey_top1000))]

        df = pd.DataFrame(columns=['name', 'rating', 'votes', 'whisky_dt', 'whisky_dd', 'review','reivewer'])

        #이후 이름, 평점, 평가 수, 위스키 정보, 리뷰, 리뷰한 사람들을 크롤링
        for idx in tqdm(range(len(url_list))):
            self.driver.get(url_list[idx])
            name = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky"]//div[@class="name "]//header')
            rating = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky"]//div[@id="whisky-details-sidebar"]//div[@id="partial-aggregate-rating"]//dl[1]//*[@class="votes-rating"]//span[1]')
            votes = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky"]//div[@id="whisky-details-sidebar"]//div[@id="partial-aggregate-rating"]//dl[1]//*[@class="votes-count"]')
            whiskey_dt = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky"]//div[@id="whisky-details"]//div[@class="block-desc"]//dl//dt')
            whiskey_dd = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky"]//div[@id="whisky-details"]//div[@class="block-desc"]//dl//dd')
            review = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky-note-holder"]//div[@class="block-notes"]//div[@id="whisky-notes"]//li//div[@class="wb--note-content-wrapper"]')
            reviewer = self.driver.find_elements(By.XPATH, '//body//div[@id="whisky-note-holder"]//div[@class="block-notes"]//div[@id="whisky-notes"]//li//h5[@class="wb--note-title"]')
            df.loc[idx] = [name[0].text, rating[0].text, votes[0].text, [whiskey_dt[x].text for x in range(len(whiskey_dt))], [whiskey_dd[x].text for x in range(len(whiskey_dd))],[review[x].text for x in range(len(review))], [reviewer[x].text for x in range(len(reviewer))]]
        #이후 csv로 저장
        df.to_csv('./data/whiskeybase_raw.csv')

    def raw_data_preprocessing(self) -> None:
        '''크롤링한 데이터는 날 것의 데이터이기에 데이터 전처리 전에 데이터 가공을 해주는 함수'''
        #csv 파일 읽기
        whiskey_df = pd.read_csv('./data/whiskeybase_raw.csv').drop(columns=['Unnamed: 0'])

        #이상한 자료형 변환
        for idx in range(len(whiskey_df)):
            for column in ['whisky_dt','whisky_dd','review','reivewer']:
                tmp = ast.literal_eval(whiskey_df[column][idx])
                whiskey_df[column][idx] = tmp

        #데이터프레임 컬럼 정의
        whiskey_info_list = ['Whiskybase ID','Category','Distillery','Bottler','Bottling serie',
                            'Vintage','Bottled','Stated Age','Casktype','Casknumber',
                            'Number of bottles','Strength','Size','Label','Bottle code',
                            'Bottled for','Market','Added on']
        whiskey_info = {'Whiskybase ID':[],'Category':[],'Distillery':[],'Bottler':[],'Bottling serie':[],
                            'Vintage':[],'Bottled':[],'Stated Age':[],'Casktype':[],'Casknumber':[],
                            'Number of bottles':[],'Strength':[],'Size':[],'Label':[],'Bottle code':[],
                            'Bottled for':[],'Market':[],'Added on':[]}

        #whiskey_dt, whiskey_dd를 위의 컬럼으로 바꿔준다.
        for idx in range(len(whiskey_df)):
            for list_idx in range(len(whiskey_df['whisky_dt'][idx])):
                if whiskey_df['whisky_dt'][idx][list_idx] in whiskey_info_list:
                    whiskey_info[whiskey_df['whisky_dt'][idx][list_idx]].append(whiskey_df['whisky_dd'][idx][list_idx])
            for list_idx in range(len(whiskey_info_list)):
                if len(whiskey_info[whiskey_info_list[list_idx]]) != idx+1:
                    whiskey_info[whiskey_info_list[list_idx]].append(np.NaN)

        
        renew_whiskey_df = pd.concat([whiskey_df, pd.DataFrame(whiskey_info)], axis=1)
        renew_whiskey_df.drop(columns=['whisky_dt','whisky_dd'], inplace=True)
        renew_whiskey_df['review_count'] = renew_whiskey_df['review'].apply(lambda x : len(x))


        #리뷰처리 
        reviewer_name = []
        reviewer_score = []
        for idx in range(len(renew_whiskey_df)):
            tmp_name = []
            tmp_score = []
            for review_idx in range(len(renew_whiskey_df['reivewer'][idx])):
                tmp_name.append(renew_whiskey_df['reivewer'][idx][review_idx].split(' ')[0])
                tmp_score.append(re.sub(r'[^0-9]', '', ''.join(renew_whiskey_df['reivewer'][idx][review_idx].split(' ')[1:])))
            reviewer_name.append(tmp_name)
            reviewer_score.append(tmp_score)
        renew_whiskey_df['reviewer_name'] = reviewer_name
        renew_whiskey_df['reviewer_score'] = reviewer_score
        renew_whiskey_df.drop(columns=['reivewer'], inplace=True)
        renew_whiskey_df=renew_whiskey_df.loc[renew_whiskey_df['review_count']!=0].reset_index().drop(columns=['index'])


        #필요없는 컬럼 제거
        #casktype 이거 중요한 피쳐같음, Distillery를 통해 위스키 만드는 곳 피쳐 엔지니어링
        renew_whiskey_df.drop(columns=['Bottler','Vintage','Bottling serie','Casknumber','Number of bottles','Label','Bottle code','Bottled for','Market','Added on'], inplace=True)

        renew_whiskey_df.to_csv('./data/whiskeybase.csv', index=False)