from math import sqrt
import random
from PIL import Image
import numpy as np


def get_points(image_path):
    img = Image.open(image_path)
    img.thumbnail((200, 400))
    img = img.convert("RGB")
    w, h = img.size
    points = []

    for count, color in img.getcolors(w * h):
        for _ in range(count):
            points.append(Point(color))

    return points


def euclidean(p, q):
    n_dim = len(p.coordinates)

    return sqrt(sum([
        (p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)
    ]))


class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates


class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.points = points


class KMeans:
    def __init__(self, n_clusters, min_diff=3):
        self.n_clusters = n_clusters
        self.min_diff = min_diff
        init: 'kmeans++'

    def calculate_center(self, points):
        n_dim = len(points[0].coordinates)
        vals = [0.0 for i in range(n_dim)]
        for p in points:

            for i in range(n_dim):
                vals[i] += p.coordinates[i]
        coords = [(v / len(points)) for v in vals]

        return Point(coords)

    def assign_points(self, clusters, points):
        point_lists = [[] for i in range(self.n_clusters)]

        for p in points:
            smallest_distance = float('inf')

            for i in range(self.n_clusters):
                distance = euclidean(p, clusters[i].center)

                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            point_lists[idx].append(p)

        return point_lists

    def fit(self, points):
        clusters = [Cluster(center=p, points=[p])
                    for p in random.sample(points, self.n_clusters)]
        while True:
            point_lists = self.assign_points(clusters, points)
            diff = 0

            for i in range(self.n_clusters):
                if not point_lists[i]:
                    continue
                old = clusters[i]
                center = self.calculate_center(point_lists[i])
                new = Cluster(center, point_lists[i])
                clusters[i] = new
                diff = max(diff, euclidean(old.center, new.center))

            if diff < self.min_diff:
                break

        return clusters


def rgb_to_hex(rgb):
    return '%s' % ''.join(('%02x' % p for p in rgb))


def get_colors(filename, n_colors=8):
    jpg = Image.open(filename)
    points = get_points(filename)
    clusters = KMeans(n_clusters=n_colors).fit(points)
    clusters.sort(key=lambda c: len(c.points), reverse=True)
    rgbs = [map(int, c.center.coordinates) for c in clusters]
    color_list = list(map(rgb_to_hex, rgbs))
    return color_list
