import time
from collections import namedtuple

import numpy as np
from scipy.spatial import KDTree

import lib

Point = namedtuple("Point", ["x", "y", "z"])


def parse_inputs(input: str):
    parsed_input = [
        Point(int(line.split(",")[0]), int(line.split(",")[1]), int(line.split(",")[2]))
        for line in input.splitlines()
    ]
    return parsed_input


def two_closest_points(tree, points):
    circuits = []
    distances, indices = tree.query(points, k=len(points))
    indices = indices[distances > 0]  # .reshape((len(points), -1))
    distances = distances[distances > 0]  # .reshape((len(points), -1))
    current_mins = np.argpartition(distances, 0)
    current_mins = np.argsort(distances)
    # for i in range(1000):
    while max(circuits) > 0:
        current_min = current_mins[i * 2 + 1]
        p1_i = current_min // (len(points) - 1)
        p2_i = indices[current_min]
        p1, p2 = int(p1_i), int(p2_i)  # points[p1_i], points[p2_i]

        added = False
        add_i, add_j = None, None
        # print(p1, p2)
        for i in range(len(circuits)):
            both = 0
            c = circuits[i]
            if p1 in c:
                both += 1
                if p2 not in c:
                    c.append(p2)
                    added = True
                    add_i = i
            if p2 in c:
                both += 1
                if p1 not in c:
                    c.append(p1)
                    added = True
                    add_j = i
            if both == 2:
                added = True

        if add_i and add_j:
            for i in circuits[add_i]:
                for j in circuits[add_j]:
                    if j not in circuits[add_i]:
                        circuits[add_i].append(j)
            del circuits[add_j]

        if not added:
            circuits.append([p1, p2])
        # print(circuits)
        # print()
    circuits = sorted(circuits, key=lambda c: len(c), reverse=True)
    # print(circuits)
    # print(len(circuits[0]) * len(circuits[1]) * len(circuits[2]))
    # print(len(circuits))
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])


def run(points, part: int):
    answer = 0
    circuits = {i: [i] for i in range(len(points))}
    tree = KDTree(points)
    answer = two_closest_points(tree, points)
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 40 if part == 1 else 0
    test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

    input = test_input if test else lib.read_input(day, part, False)
    parsed_input = parse_inputs(input)
    start = time.perf_counter()
    answer = run(parsed_input, part)
    end = time.perf_counter()
    if test:
        assert answer == test_answer, (
            f"\nTest answer: {test_answer}\nMy answer: {answer}"
        )
        if answer == test_answer:
            print(f"Test passed! {test_answer} = {answer}")
    else:
        print(f"My answer: {answer}")
    print(f"Took: {end - start:.6f} seconds")
    return
