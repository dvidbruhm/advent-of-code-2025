import math
import time
from dataclasses import dataclass, field

import lib


def rotate_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]


@dataclass
class Problem:
    nums: list[int] = field(default_factory=list)
    op: str = ""

    def answer(self):
        if self.op == "+":
            return sum(self.nums)
        return math.prod(self.nums)


def parse_inputs(input: str, part: int):
    problems = []

    lines = input.splitlines()
    num_cols = len(lines[0].split())
    for col in range(num_cols):
        problems.append(Problem())

    if part == 2:
        grid = rotate_matrix([list(line) for line in lines])
        i = 0
        for line in grid:
            if all([c == " " for c in line]):
                i += 1
                continue
            line = list(filter(lambda c: c != " ", line))
            if line[-1] in ("+", "*"):
                problems[i].op = line[-1]
                line = line[:-1]
            problems[i].nums.append(int("".join(line)))

    else:
        for row, line in enumerate(lines):
            for col, data in enumerate(line.split()):
                if row < len(lines) - 1:
                    problems[col].nums.append(int(data))
                else:
                    problems[col].op = data

    return problems


def run(problems, part: int):
    answer = sum([p.answer() for p in problems])
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 4277556 if part == 1 else 3263827
    test_input = lib.read_input("6_test", part, False)

    input = test_input if test else lib.read_input(day, part, False)
    parsed_input = parse_inputs(input, part)
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
