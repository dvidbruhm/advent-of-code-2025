import argparse
import importlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", required=True, type=int)
    parser.add_argument("-p", "--part", required=True, type=int)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-g", "--debug", action="store_true")
    args = parser.parse_args()

    day = importlib.import_module(f"day{args.day}")
    day.main(args.day, args.part, args.test, args.debug)


if __name__ == "__main__":
    main()
