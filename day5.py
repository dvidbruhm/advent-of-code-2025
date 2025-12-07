import time
from dataclasses import dataclass

import lib


@dataclass
class Range:
    start: int
    end: int
    active: bool = True

    def inrange(self, num: int):
        return num >= self.start and num <= self.end


def parse_inputs(input: str):
    ranges = [
        Range(int(line.split("-")[0]), int(line.split("-")[1]))
        for line in input.split("\n\n")[0].splitlines()
    ]
    ingredients = [int(line) for line in input.split("\n\n")[1].splitlines()]

    return (ranges, ingredients)


def run(parsed_input, part: int):
    answer = 0
    ranges, ingredients = parsed_input

    if part == 1:
        for id in ingredients:
            for r in ranges:
                if r.inrange(id):
                    answer += 1
                    break
    else:
        for i in range(len(ranges)):
            for j in range(i + 1, len(ranges)):
                r1, r2 = ranges[i], ranges[j]
                if r1.start <= r2.start <= r1.end and r1.start <= r2.end <= r1.end:
                    r2.active = False
                elif r2.start <= r1.start <= r2.end and r2.start <= r1.end <= r2.end:
                    r1.active = False
                elif r1.start <= r2.start <= r1.end and r2.end >= r1.end:
                    r2.start = r1.end + 1
                elif r1.start <= r2.end <= r1.end and r2.start <= r1.start:
                    r2.end = r1.start - 1
        for r in ranges:
            if not r.active:
                continue
            answer += r.end - r.start + 1

    return answer


def main(day: int, part: int, test: bool):
    test_answer = 3 if part == 1 else 14
    test_input = """3-5
10-14
16-20
13-17
1-20

1
5
8
11
17
32
"""

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
