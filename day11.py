import time

import networkx as nx

import lib


def parse_inputs(input: str):
    G = nx.DiGraph()
    connections = {}
    for line in input.splitlines():
        fr = line.split(":")[0]
        to = line.split(":")[1].split(" ")[1:]
        for t in to:
            G.add_edge(fr, t)
        input, outputs = line.split(": ")
        connections[input] = outputs.split()
    return G, connections


def run(input, part: int, debug: bool):
    G, connections = input

    c = {}

    def dfs(node, fft, dac):
        global n_paths
        key = (node, fft, dac)
        if key in c:
            return c[key]

        if node == "out":
            c[key] = 1 if fft and dac else 0
            return c[key]

        outputs = connections.get(node)
        if outputs is None:
            c[key] = 0
            return 0

        if node == "fft":
            fft = True
        elif node == "dac":
            dac = True

        s = 0
        for out in outputs:
            c[(out, fft, dac)] = dfs(out, fft, dac)
            s += c[(out, fft, dac)]

        return s

    start_node = "you" if part == 1 else "svr"
    end_node = "out"

    if part == 1:
        paths = list(nx.all_simple_paths(G, start_node, end_node))
        answer = len(paths)
    else:
        answer = dfs("svr", False, False)

    return answer


def main(day: int, part: int, test: bool, debug: bool):
    test_answer = 5 if part == 1 else 2
    test_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

    if part == 2:
        test_input = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

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
