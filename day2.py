import time

import lib

num_map = {
    2: [1],
    3: [1],
    4: [1, 2],
    5: [1],
    6: [1, 2, 3],
    7: [1],
    8: [1, 2, 4],
    9: [1, 3],
    10: [1, 2, 5],
}


def parse_inputs(input: str):
    parsed_input = []
    for s1 in input.split(","):
        s2 = s1.split("-")
        start, end = s2[0], s2[1]
        parsed_input.append((start, end))
    return parsed_input


def run(parsed_input, part: int):
    answer = 0
    is_invalid = is_invalid_part1 if part == 1 else is_invalid_part2
    for pair in parsed_input:
        start, end = pair[0], pair[1]
        start_even, end_even = len(start) % 2 == 0, len(end) % 2 == 0
        if not start_even and not end_even and len(start) == len(end) and part == 1:
            continue
        for id in range(int(start), int(end) + 1):
            s_id = str(id)
            if len(s_id) % 2 == 1 and part == 1:
                continue
            if is_invalid(s_id):
                answer += int(s_id)
    return answer


def is_invalid_part1(id: str):
    return id[0 : len(id) // 2] == id[len(id) // 2 :]


def is_invalid_part2(id: str):
    id_len = len(id)
    if id_len == 1:
        return False
    ms = num_map[id_len]
    invalid = False
    for m in ms:
        for i in range(0, id_len - m, m):
            if id[i : i + m] != id[i + m : (i + m * 2)]:
                break
        else:
            invalid = True
            return invalid

    return invalid


def main(day: int, part: int, test: bool):
    test_answer = 1227775554 if part == 1 else 4174379265
    test_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
    1698522-1698528,446443-446449,38593856-38593862,565653-565659,
    824824821-824824827,2121212118-2121212124"""

    input = test_input if test else lib.read_input(day, part, False)
    parsed_input = parse_inputs(input)
    start = time.perf_counter()
    answer = run(parsed_input, part)
    end = time.perf_counter()
    if test:
        assert answer == test_answer, (
            f"\nFAIL\nTest answer: {test_answer}\nMy answer: {answer}"
        )
        if answer == test_answer:
            print(f"Test passed! {test_answer} = {answer}")
    print(f"My answer: {answer}")
    print(f"Took: {end - start:.6f} seconds")
    return
