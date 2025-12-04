import time

import lib


def parse_inputs(input: str):
    parsed_input = []
    for line in input.splitlines():
        parsed_input.append([int(c) for c in line])
    return parsed_input


def run(parsed_input, part: int):
    answer = 0
    for bank in parsed_input:
        maxs = joltage(bank, 2 if part == 1 else 12)
        answer += int("".join([str(c) for c in maxs]))

    return answer


def joltage(bank: list[int], n_digits: int):
    maxs = []
    i = 0

    lookup = len(bank) - n_digits
    while len(maxs) < n_digits:
        m = max(bank[i : i + lookup + 1])
        m_i = bank[i : i + lookup + 1].index(m)
        i = i + m_i + 1
        maxs.append(m)
        lookup = lookup - m_i

    return maxs


def main(day: int, part: int, test: bool):
    test_answer = 357 if part == 1 else 3121910778619
    test_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

    input = test_input if test else lib.read_input(day, part, False)
    parsed_input = parse_inputs(input)
    start = time.perf_counter()
    answer = run(parsed_input, part)
    end = time.perf_counter()
    if test:
        assert answer == test_answer, (
            f"\nTest answer: {test_answer}\nMy answer: {answer}"
        )
    else:
        print(f"My answer: {answer}")
        print(f"Took: {end - start:.6f} seconds")
    return
