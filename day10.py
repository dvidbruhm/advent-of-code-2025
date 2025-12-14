import itertools
import time
from collections import deque

import networkx as nx
from mpmath.libmp.gammazeta import math
from sympy import linsolve, symbols
from sympy.matrices.expressions.funcmatrix import Matrix

import lib


def parse_inputs(input: str):
    parsed_input = [
        (
            l.split(" ")[0][1:-1],
            [[int(a) for a in b[1:-1].split(",")] for b in l.split(" ")[1:-1]],
            [int(b) for b in l.split(" ")[-1][1:-1].split(",")],
        )
        for l in input.splitlines()
    ]

    return parsed_input


def push_button(lights, button):
    for light in button:
        lights = (
            lights[:light]
            + ("." if lights[light] == "#" else "#")
            + lights[light + 1 :]
        )
    return lights


def push_button_joltage(button, joltages):
    for b in button:
        joltages[b] += 1
    return joltages


def check_joltages(joltages, potential_joltages):
    for i in range(len(joltages)):
        if potential_joltages[i] > joltages[i]:
            return False
    return True


def run(machines, part: int, debug: bool):
    answer = 0

    if part == 1:
        for lights, buttons, joltages in machines:
            G = nx.Graph()
            new_nodes = deque()
            new_nodes.append("." * len(lights))
            while new_nodes:
                current_lights = new_nodes.pop()
                for button in buttons:
                    potential_node = push_button(current_lights, button)
                    if potential_node not in list(G.nodes):
                        new_nodes.append(potential_node)
                    G.add_edge(current_lights, potential_node)
            path = next(nx.shortest_simple_paths(G, "." * len(lights), lights))
            answer += (
                len(next(nx.shortest_simple_paths(G, "." * len(lights), lights))) - 1
            )
    else:
        iiii, mmm = 1, len(machines)
        for lights, buttons, joltages in machines:
            if debug:
                print()
                print(f"{iiii} / {mmm}")
            iiii += 1
            ns = symbols(" ".join(["n" + str(i) for i in range(len(buttons))]))

            system = []
            symbols_asso = {
                s: min([joltages[a] for a in buttons[i]]) for i, s in enumerate(ns)
            }
            # print(symbols_asso)
            for i, j in enumerate(joltages):
                s = []
                for b in buttons:
                    s.append(1 if i in b else 0)
                s.append(j)
                system.append(s)
            system = Matrix(system)
            # print(ns)
            if debug:
                print(system)

            solution = linsolve(system, ns)
            if debug:
                print(solution)
            max_s = []
            free_syms = solution.args[0].free_symbols
            # print(free_syms)
            for fs in free_syms:
                max_s.append(symbols_asso[fs])

            if debug:
                print(free_syms)
                print(max_s)

            min_res = math.inf
            all_combos = itertools.product(*[list(range(0, m + 1)) for m in max_s])
            for nums in all_combos:
                # print(nums)

                res = [
                    eq.evalf(subs={fs: nums[i] for i, fs in enumerate(free_syms)})
                    for eq in solution.args[0]
                ]

                # print(res)

                if any(num < 0 for num in res):
                    continue

                sum_res = int(sum(res))
                min_res = sum_res if sum_res < min_res else min_res
                # print(sum_res, min_res)
            answer += min_res
            # print(solution.args[0][0].evalf(subs={ns[3]: 1, ns[5]: 1}))

    return answer


def main(day: int, part: int, test: bool, debug: bool):
    test_answer = 7 if part == 1 else 33
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    input = test_input if test else lib.read_input(day, part, False)
    parsed_input = parse_inputs(input)
    start = time.perf_counter()
    answer = run(parsed_input, part, debug)
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
