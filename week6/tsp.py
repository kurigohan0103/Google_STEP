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

# ルートの一部をスワップする3-optスワップ関数
def swap_3opt(route, i, j, k):
    new_routes = [
        route[:i] + route[i:j + 1][::-1] + route[j + 1:k + 1][::-1] + route[k + 1:],
        route[:i] + route[j + 1:k + 1] + route[i:j + 1] + route[k + 1:],
        route[:i] + route[j + 1:k + 1][::-1] + route[i:j + 1] + route[k + 1:],
        route[:i] + route[i:j + 1] + route[j + 1:k + 1] + route[k + 1:]
    ]
    return new_routes

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

# 2.5-optアルゴリズムを適用してルートを最適化する関数
def opt_2_5(points, route):
    improvement = True  # 改善があったかどうかを示すフラグ
    while improvement:
        improvement = False
        best_distance = total_distance(points, route)  # 現在のルートの総距離を計算
        # ルートのすべての2点間についてスワップを試行
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                for k in range(j + 1, len(route)):
                    # Perform 2-opt swap
                    new_route_2opt = swap_2opt(route, i, j)
                    new_distance_2opt = total_distance(points, new_route_2opt)
                    # Perform 3-opt swap
                    new_routes_3opt = swap_3opt(route, i, j, k)
                    new_distances_3opt = [total_distance(points, new_route) for new_route in new_routes_3opt]
                    # Check for improvements
                    if new_distance_2opt < best_distance:
                        route = new_route_2opt
                        best_distance = new_distance_2opt
                        improvement = True
                    for idx, new_distance in enumerate(new_distances_3opt):
                        if new_distance < best_distance:
                            route = new_routes_3opt[idx]
                            best_distance = new_distance
                            improvement = True
    return route


def solve(cities):
    initial_route = greedy_initial_route(cities)  # 初期ルートを生成
    optimized_route = opt_2_5(cities, initial_route)  # 2.5-opt
    return optimized_route


if __name__ == '__main__':
   assert len(sys.argv) > 1
   tour = solve(read_input(sys.argv[1]))
   print_tour(tour)
