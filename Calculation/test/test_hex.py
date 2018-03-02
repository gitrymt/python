# -*- coding: utf-8 -*-
"""
Test plot of Bri

Created on Fri Feb 23 23:13:58 2018
@author: gitrymt
"""

# 六角形のグリッドを描画する

import numpy as np
import matplotlib.pyplot as plt

# hexgridの縦横サイズ
PX=1
PY = PX * np.sqrt(3)/2

# 一辺の長さ
L = PX / np.sqrt(3)



def main():
    # 検証用座標列:縦横5個づつ
    mesh_list = [[x,y] for x in range(5) for y in range(1)]

    # グラフ描画
    for x, y in mesh_list:

        # 座標中心を計算
        cx = x*PX if y%2==0 else (x+0.5)*PX
        cy = y*PY
        # 中心点の描画
#        an = '$\Gamma$'
#        plt.plot(cx, cy, 'ok')
        # 六角形の描画
        plotBrillouinZone_tri(cx, cy)

    # グラフ描画
    plt.show()

if __name__ == '__main__':
    main()