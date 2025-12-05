import time

import lib


def parse_inputs(input: str):
    parsed_input = []
    return parsed_input


def run(parsed_input, part: int):
    answer = 0

    return answer


def main(day: int, part: int, test: bool):
    test_answer = 0 if part == 1 else 0
    test_input = """
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
