import time
from collections import namedtuple

import numpy as np
from line_profiler import profile
from scipy.spatial import KDTree

import lib

Point = namedtuple("Point", ["x", "y", "z"])


def parse_inputs(input: str):
    parsed_input = [
        Point(int(line.split(",")[0]), int(line.split(",")[1]), int(line.split(",")[2]))
        for line in input.splitlines()
    ]
    return parsed_input


@profile
def update_circuits(circuits, p1, p2):
    # Slow set intersection/union method, but simple and works
    circuits.append(set([p1, p2]))
    for _ in range(2):
        to_remove = []
        for i in range(len(circuits)):
            for j in range(i + 1, len(circuits)):
                if len(circuits[i].intersection(circuits[j])) > 0:
                    circuits[i] = circuits[i].union(circuits[j].difference(circuits[i]))
                    to_remove.append(circuits[j])
        for r in to_remove:
            if r in circuits:
                circuits.remove(r)
    return


def end_cond(circuits, size, i, part, test):
    if part == 1:
        end_i = 1000 if not test else 10
        return i >= end_i

    if len(circuits) == 0:
        return False
    return len(max(circuits, key=lambda c: len(c))) >= size


def run(points, part: int, test: bool):
    answer = 0
    circuits = []
    size = len(points)

    tree = KDTree(points)
    distances, indices = tree.query(points, k=len(points))
    indices = indices[distances > 0]
    distances = distances[distances > 0]
    current_mins = np.argsort(distances)

    i = 0
    p1_i, p2_i = 0, 0
    while not end_cond(circuits, size, i, part, test):
        current_min = current_mins[i * 2 + 1]
        p1_i, p2_i = current_min // (len(points) - 1), indices[current_min]
        p1, p2 = int(p1_i), int(p2_i)

        update_circuits(circuits, p1, p2)
        i += 1

    circuits = sorted(circuits, key=lambda c: len(c), reverse=True)

    if part == 1:
        answer = len(circuits[0]) * len(circuits[1]) * len(circuits[2])
    else:
        answer = points[p1_i].x * points[p2_i].x
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 40 if part == 1 else 25272
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
    answer = run(parsed_input, part, test)
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
