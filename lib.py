def read_input(day: int, part: int, use_part: bool = False):
    file_name = f"input{day}.txt"
    if use_part:
        file_name = f"input{day}_{part}.txt"

    with open(file_name, "r") as f:
        text = f.read()

    return text
