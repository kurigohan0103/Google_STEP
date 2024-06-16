#!/usr/bin/env python3

import sys
import math
import csv
from common import print_tour, read_input


def calculate_distance(points, i, j):
    x1, y1 = points[i]
    x2, y2 = points[j]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def total_distance(points, route):
    total_dist = 0
    num_points = len(route)

    for i in range(num_points):
        start = route[i]
        end = route[(i + 1) % num_points]
        dist = calculate_distance(points, start, end)
        total_dist += dist

    return total_dist


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


def solve(cities):
    initial_route = greedy_initial_route(cities)
    optimized_route = apply_2opt(cities, initial_route)
    return optimized_route


def write_output(file_name, tour):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["index"])
        for city in tour:
            writer.writerow([city])


if __name__ == '__main__':
    for i in range(7):
        input_file = f'input_{i}.csv'
        output_file = f'output_{i}.csv'

        cities = read_input(input_file)
        tour = solve(cities)
        write_output(output_file, tour)

        # スコアを計算して表示
        score = total_distance(cities, tour)
        print(f"Challenge {i}: Total distance (score): {score}")
