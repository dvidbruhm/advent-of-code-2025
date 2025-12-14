import time
from collections import namedtuple

import lib

Point = namedtuple("Point", ["x", "y"])


def parse_inputs(input: str):
    parsed_input = [
        Point(int(l.split(",")[0]), int(l.split(",")[1])) for l in input.splitlines()
    ]
    return parsed_input


def area(p1: Point, p2: Point):
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)


def valid(points, p1, p2, part):
    if part == 1:
        return True


def run(points, part: int):
    max_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if not valid(points, points[i], points[j], part):
                continue
            a = area(points[i], points[j])
            max_area = max_area if a < max_area else a
    answer = max_area
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 50 if part == 1 else 0
    test_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

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
