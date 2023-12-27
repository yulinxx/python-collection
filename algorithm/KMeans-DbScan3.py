# https://github.com/garoriz/dbScan

# DB-SCAN是一个基于密度的聚类。不规则形态的点，如果用K-Means，效果不会很好。
# 而通过DB-SCAN就可以很好地把在同一密度区域的点聚在一类中。


import random
from itertools import cycle

import numpy as np
import pygame
from numpy import random


def dist(pointA, pointB):
    return np.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


def near_points(point):
    count = random.randint(2, 5)
    points_array = []
    for i in range(count):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        points_array.append((point[0] + x, point[1] + y))
    return points_array


def is_yellow_point(n, alone_points):
    if n not in alone_points:
        return True
    return False


def iterate_for_neighbours(p, neighbours, alone_points):
    is_yellow = False
    for n in neighbours:
        is_yellow = is_yellow_point(n, alone_points)
    if is_yellow:
        pygame.draw.circle(screen, color='yellow', center=p, radius=5)
    else:
        pygame.draw.circle(screen, color='red', center=p, radius=5)


def draw_red_points(p, neighbours, alone_points):
    if len(neighbours) == 1:
        pygame.draw.circle(screen, color='red', center=p, radius=5)
    else:
        iterate_for_neighbours(p, neighbours, alone_points)


def dbscan(points_array, distance, count_of_points, scr):
    alone = 0
    pointer = 0

    visited_points = set()
    clustered_points = set()
    cluster_map = {alone: []}

    def find_neighbours(p):
        return [q for q in points_array if dist(p, q) < distance]

    def add_cluster(point, n):
        if pointer not in cluster_map:
            cluster_map[pointer] = []
        cluster_map[pointer].append(point)
        clustered_points.add(point)
        while n:
            q = n.pop()
            if q not in visited_points:
                visited_points.add(q)
                pygame.draw.circle(scr, color='green', center=q, radius=5)
                neighbours2 = find_neighbours(q)
                if len(neighbours2) > count_of_points:
                    n.extend(neighbours2)
            if q not in clustered_points:
                clustered_points.add(q)
                cluster_map[pointer].append(q)
                if q in cluster_map[alone]:
                    cluster_map[alone].remove(q)

    for p in points_array:
        if p in visited_points:
            continue
        visited_points.add(p)
        neighbours = find_neighbours(p)
        if len(neighbours) < count_of_points:
            cluster_map[alone].append(p)
        else:
            pointer += 1
            add_cluster(p, neighbours)
            # plt.scatter(p[0], height - p[1], c='g')
            pygame.draw.circle(scr, color='green', center=p, radius=5)

    for p in cluster_map[alone]:
        neighbours = find_neighbours(p)
        draw_red_points(p, neighbours, cluster_map[alone])

    return cluster_map


if __name__ == '__main__':
    HEIGHT = 400
    pygame.init()
    screen = pygame.display.set_mode((600, HEIGHT))
    screen.fill(color="#FFFFFF")
    pygame.display.update()
    is_active = True
    is_pressed = False
    points = []
    count_of_keyup = 0
    clusters = {}
    while (is_active):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_pressed = True
                if event.button == 1:
                    is_pressed = True
                    coord = event.pos
                    points.append(coord)
                    pygame.draw.circle(screen, color='black', center=coord, radius=5)
            if event.type == pygame.MOUSEBUTTONUP:
                is_pressed = False
            if event.type == pygame.MOUSEMOTION:
                if is_pressed:
                    # if random.choice((0,10))==0:
                    # coord = event.pos
                    # pygame.draw.circle(screen, color='black', center=coord, radius=10)
                    if dist(event.pos, points[-1]) > 20:
                        coord = event.pos
                        pygame.draw.circle(screen, color='black', center=coord, radius=5)
                        for nearP in near_points(coord):
                            pygame.draw.circle(screen, color='black', center=nearP, radius=5)
                            points.append(nearP)
                        points.append(coord)
            if event.type == pygame.KEYUP:
                if event.key == 13:
                    count_of_keyup = count_of_keyup + 1
                    if count_of_keyup == 1:
                        clusters = dbscan(points, 50, 4, screen)
                    else:
                        for colour, points in zip(cycle(["blue", "green", "red", "yellow", "grey", "black"]), clusters.values()):
                            points_in_one_group = [p for p in points]
                            for p in points_in_one_group:
                                pygame.draw.circle(screen, color=colour, center=p, radius=5)

        pygame.display.update()