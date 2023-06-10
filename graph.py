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
