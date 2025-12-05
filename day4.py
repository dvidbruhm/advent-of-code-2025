import time

import lib

dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]


def parse_inputs(input: str):
    parsed_input = []
    x, y = 0, 0
    for c in input:
        if c == "@":
            parsed_input.append((x, y))
        if c == "\n":
            x = 0
            y += 1
        else:
            x += 1
    return set(parsed_input)


def check_neighbors(x: int, y: int, grid):
    nb_neighbors = 0
    for dx, dy in dirs:
        nb_neighbors += 1 if (x + dx, y + dy) in grid else 0
    return nb_neighbors


def run_once(parsed_input, part: int):
    answer = 0
    to_remove = []
    for x, y in parsed_input:
        nb_neighbors = check_neighbors(x, y, parsed_input)
        if nb_neighbors < 4:
            answer += 1
            to_remove.append((x, y))
    return answer, to_remove


def run(parsed_input, part: int):
    answer = 0
    current_run = -1

    while current_run != 0:
        current_run, to_remove = run_once(parsed_input, part)
        answer += current_run
        parsed_input.difference_update(to_remove)
        if part == 1:
            break
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 13 if part == 1 else 43
    test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

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
