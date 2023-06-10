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