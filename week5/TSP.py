import numpy as np


def calculate_distance(points, i, j):

    return np.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)


def total_distance(points, route):

    return sum(calculate_distance(points, route[i], route[(i + 1) % len(route)]) for i in range(len(route)))


def swap_2opt(route, i, k):

    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]


def greedy_initial_route(points):

    n = len(points)
    start = 0
    unvisited = set(range(n))
    unvisited.remove(start)
    route = [start]
    current = start

    while unvisited:
        next_city = min(unvisited, key=lambda city: calculate_distance(points, current, city))
        unvisited.remove(next_city)
        route.append(next_city)
        current = next_city

    return route


def apply_2opt(points, route):
    improvement = True
    while improvement:
        improvement = False
        best_distance = total_distance(points, route)
        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = swap_2opt(route, i, k)
                new_distance = total_distance(points, new_route)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improvement = True
    return route


# Example
points = np.random.rand(10, 2)  # 10個のランダムな点を生成
route = greedy_initial_route(points)  # 貪欲法で初期ルートを生成
optimized_route = apply_2opt(points, route)  # 2-optアルゴリズムでルートを最適化
print("Optimized route:", optimized_route)

