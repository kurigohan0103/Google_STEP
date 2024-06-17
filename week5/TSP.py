#!/usr/bin/env python3

import sys
import math
import csv
from common import print_tour, read_input

# 2点間の距離を計算する関数
def calculate_distance(points, i, j):
    x1, y1 = points[i]
    x2, y2 = points[j]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# ルート全体の総距離を計算する関数
def total_distance(points, route):
    total_dist = 0
    num_points = len(route)

    # 各都市間の距離を計算し、合計する
    for i in range(num_points):
        start = route[i]
        end = route[(i + 1) % num_points]  # ルートを循環させる
        dist = calculate_distance(points, start, end)
        total_dist += dist

    return total_dist

# ルートの一部を逆順にする2-optスワップ関数
def swap_2opt(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

# 初期ルートを生成する関数
def greedy_initial_route(points):
    n = len(points)
    start = 0  # 開始地点
    unvisited = set(range(n))  # 未訪問の都市集合
    unvisited.remove(start)
    route = [start]
    current = start

    # すべての都市を訪問するまでループ
    while unvisited:
        # 現在の都市から最も近い未訪問の都市を選択
        next_city = min(unvisited, key=lambda city: calculate_distance(points, current, city))
        unvisited.remove(next_city)  # 選択した都市を未訪問リストから削除
        route.append(next_city)
        current = next_city  # 現在の都市を更新

    return route

# 2-optアルゴリズムを適用してルートを最適化する関数
def 2opt(points, route):
    improvement = True  # 改善があったかどうかを示すフラグ
    while improvement:
        improvement = False
        best_distance = total_distance(points, route)  # 現在のルートの総距離を計算
        # ルートのすべての2点間についてスワップを試行
        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = swap_2opt(route, i, k)  # ルートの一部を逆順にする
                new_distance = total_distance(points, new_route)  # 新しいルートの総距離を計算
                # 新しいルートが改善されている場合
                if new_distance < best_distance:
                    route = new_route  # ルートを更新
                    best_distance = new_distance  # 最良距離を更新
                    improvement = True  # 改善フラグを立てる
    return route


def solve(cities):
    initial_route = greedy_initial_route(cities)  # 初期ルートを生成
    optimized_route = 2opt(cities, initial_route)  # 2-opt
    return optimized_route


if __name__ == '__main__':
   assert len(sys.argv) > 1
   tour = solve(read_input(sys.argv[1]))
   print_tour(tour)
