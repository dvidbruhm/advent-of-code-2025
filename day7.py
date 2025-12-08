import time
from collections import namedtuple

import lib

# @dataclass
# class Beam:
#     x: int
#     y: int

#     def udpate(self, grid):
#         pass


Beam = namedtuple("Beam", ["x", "y"])


def parse_inputs(input: str):
    splitters = []
    beams = []

    x, y = 0, 0
    for c in input:
        if c == "^":
            splitters.append((x, y))
        elif c == "S":
            beams.append(Beam(x, y))

        if c == "\n":
            x = 0
            y += 1
        else:
            x += 1

    size = (len(input.splitlines()[0]), len(input.splitlines()))
    beams_dict = {i: 0 for i in range(size[0])}
    beams_dict[beams[0].x] = 1

    return (beams_dict, set(splitters), size)


def print_line(beams, splitters, size, y):
    for x in range(size[0]):
        current = Beam(x, y)
        if current in beams:
            print("|", end="")
        elif current in splitters:
            print("^", end="")
        else:
            print(".", end="")
    print(f"{len(beams)} {y}/{size[1]}", end="")


def step(beams, splitters, size, y, part):
    n_beams = len(beams)
    n_splits = 0
    to_remove = []
    # print_line(beams, splitters, size, y)
    # print()
    for i in range(n_beams):
        beams[i] = Beam(beams[i].x, beams[i].y + 1)

    for i in range(n_beams):
        if beams[i] in splitters:
            n_splits += 1
            to_remove.append(beams[i])
            right, left = (
                Beam(beams[i].x + 1, beams[i].y),
                Beam(beams[i].x - 1, beams[i].y),
            )
            if part == 1:
                if left not in beams and left.x >= 0:
                    beams.append(left)
                if right not in beams and right.x < size[0]:
                    beams.append(right)
            else:
                beams.append(left)
                beams.append(right)
    for r in set(to_remove):
        beams.remove(r)

    return n_splits


def step_p2(beams, splitters, size, y):
    n_splits = 0
    to_mod = []
    for beam, n in beams.items():
        if Beam(beam, y + 1) in splitters and beams[beam] > 0:
            n_splits += 1
            to_mod.append((beam, 0))
            to_mod.append((beam - 1, n))
            to_mod.append((beam + 1, n))

    for beam, n in to_mod:
        beams[beam] = n if n == 0 else beams[beam] + n
    return n_splits


def print_line2(beams, splitters, size, y):
    # print(beams.values())
    for i in range(size[0]):
        if Beam(i, y + 1) in splitters:
            print("^", end="")
        elif beams[i] > 0:
            print("|", end="")
        else:
            print(".", end="")
    print(f" {sum(beams.values())}", end="")
    [print(f" {k}:{v} ", end="") for k, v in beams.items()]
    print()


def run(parsed_input, part: int):
    answer = 0
    beams, splitters, size = parsed_input
    n_splits = [step_p2(beams, splitters, size, y) for y in range(size[1] - 1)]
    answer = sum(n_splits) if part == 1 else sum(beams.values())
    return answer


def main(day: int, part: int, test: bool):
    test_answer = 21 if part == 1 else 40
    test_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

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
