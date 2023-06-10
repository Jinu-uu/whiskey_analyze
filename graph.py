import pandas as pd
import numpy as np
import random

from matplotlib import pyplot as plt
import ast

import matplotlib.pyplot as plt
from matplotlib import gridspec
from math import pi

class graph:
    def __init__(self, graph_num = 4) -> None:
        '''결과 그래프 몇개 그릴건지 init'''
        self.graph_num = graph_num

    def make_spider(self, gs, n, color, data, number) -> None:
        '''spider 모양 그래프를 그려주는 함수(6가지 맛 시각화)'''

        categories = list(data.columns[2:])
        N = len(categories)

        #앵글 설정
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        #subplot(그래프 개수) 설정
        ax = plt.subplot(gs[n], polar=True, )

        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        #값 범위 설정
        plt.xticks(angles[:-1], categories, color='grey', size=11)

        #y라벨 범위 설정 및 제한
        ax.set_rlabel_position(0)
        plt.yticks([1, 2, 3, 4], ["0.25","0.50","0.75", "1.00"], color="grey", size=0)
        plt.ylim(0, 4)

        # spider 그래프 구현
        values=self.whiskey_variety_vectors_normalized.iloc[number,2:-1].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)

        #타이틀 달아줌
        plt.title(self.whiskey_variety_vectors_normalized['name'][number].split(',')[0], size=13, color='black', y=1.2)

    def plot_number_line(self, gs, n, dot_color, data, number) -> None:
        '''바디감을 시각화하는 함수'''
        #그래프 및 x축, y축 멈위 설정
        ax = plt.subplot(gs[n])
        ax.set_xlim(-1, 2)
        ax.set_ylim(0, 3)

        #선 draw 및 범위, 높이 설정
        xmin = 0
        xmax = 1
        y = 1
        height = 0.2

        #선 시각화
        plt.hlines(y, xmin, xmax)
        plt.vlines(xmin, y - height / 2., y + height / 2., colors='black')
        plt.vlines(xmax, y - height / 2., y + height / 2., colors='black')

        #점 시각화
        px = self.whiskey_variety_vectors_normalized['weight'][number]
        plt.plot(px, y, 'ko', ms = 10, mfc = dot_color)

        #이제 시각화한 그래프 아래에 바디감 출력
        plt.text(xmin - 0.1, y, 'Light-Bodied', horizontalalignment='right', fontsize=11, color='grey')
        plt.text(xmax + 0.1, y, 'Full-Bodied', horizontalalignment='left', fontsize=11, color='grey')

        plt.axis('off')

    def create_text(self, gs, n, data, number) -> None:
        '''위스키 향에 대한 정보를 그래프 아래에 출력해주는 함수'''
        data = list(data)
        ax = plt.subplot(gs[n])
        
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.invert_yaxis()
        
        #텍스트 만든 뒤
        text = 'Wshikey Aromas:\n'
        for x in range(len(self.whiskey_variety_vectors_normalized['relative_frequency'][number])):
            if x == 5: break
            text += self.whiskey_variety_vectors_normalized['relative_frequency'][number][x][0]
            text += '\n'
        text = text[:-1]
        #출력
        ax.text(x=0, y=1, s=text, fontsize=12, color='grey')


    def plot_whiskey_recommendations(self, data) -> None:
        '''위스키 향, 바디감, 맛 시각화 해주는 함수'''
        plt.figure(figsize=(self.graph_num*5, self.graph_num*2), dpi=96)

        gs = gridspec.GridSpec(3, self.graph_num, height_ratios=[3, 0.5, 1]) 
        self.whiskey_variety_vectors_normalized.iloc[:,1:-1]


        spider_nr = 0
        number_line_nr = self.graph_num
        descriptor_nr = self.graph_num * 2

        #랜덤 배열 생성
        pick_whiskey = [random.randrange(0,len(self.whiskey_variety_vectors_normalized)) for x in range(self.graph_num)]

        #랜덤하게 뽑은 위스키를 for문에서 시각화
        for w in range(self.graph_num):
            self.make_spider(gs, spider_nr, 'green', data.iloc[:,:-1], number=pick_whiskey[w])
            self.plot_number_line(gs, number_line_nr,dot_color='red', data=data.iloc[:,1], number=pick_whiskey[w])
            self.create_text(gs, descriptor_nr, data.iloc[:,-1], number=pick_whiskey[w])
            spider_nr += 1
            number_line_nr += 1
            descriptor_nr += 1  
        #결과 저장
        plt.savefig('./output.png')

    def normalize(self, df, cols_to_normalize) -> pd.DataFrame:
        '''데이터프레임의 모든 값들을 0~1사이로 정규화'''
        for feature_name in cols_to_normalize:
            print(feature_name)
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            df[feature_name] = df[feature_name].apply(lambda x: (x- min_value)/(max_value-min_value))
    #         (df[feature_name] - min_value) / (max_value - min_value)
        return df

    def check_in_range(self, label_range_dict, value) -> str:
        '''value 값을 받으면 정해진 범위 내로 label encording'''
        for label, value_range_tuple in label_range_dict.items():
            lower_end = value_range_tuple[0]
            upper_end = value_range_tuple[1]
            if value >= lower_end and value <= upper_end:
                return label
            else:
                continue
